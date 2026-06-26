"""
core/trainer.py — Local GPT Fine-Tuning for amber-hunter v1.2.37

用 auto-research 优化的超参（N_HEAD=1, BLOCK_SIZE=96, N_EMBED=256）
在用户记忆数据上微调，为 recall 重排 / 自动标签 / 记忆抽取提供本地推理。

增强功能 v1.2.35:
  1. WAL sessions + agent session logs 扩充训练数据
  2. TagHead 分类头支持 auto-tagging
  3. GPT-2 预训练权重初始化
  4. 增量训练（从 checkpoint 继续）
"""
from __future__ import annotations

import json, math, os, time, secrets, sys, re
from pathlib import Path
from typing import Optional

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset

# ── 路径 ─────────────────────────────────────────────────────
HOME = Path.home()
MODEL_DIR = HOME / ".amber-hunter" / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODEL_DIR / "amber-gpt.pt"
TOKENIZER_PATH = MODEL_DIR / "tokenizer.json"
TAG_VOCAB_PATH = MODEL_DIR / "tag_vocab.json"

# ── 优化超参（来自 auto-research exp_079）───────────────────
BLOCK_SIZE = 96
N_EMBED = 256
N_HEAD = 1
N_LAYER = 6
DROPOUT = 0.05
LEARNING_RATE = 1e-3
WEIGHT_DECAY = 0.0
MAX_ITERS = 300  # 每轮 fine-tune 最大迭代（5分钟 wall clock）
TAG_VOCAB_SIZE = 50  # 常用标签数量


# ── 简单 BPE Tokenizer ───────────────────────────────────────

class SimpleTokenizer:
    """
    基于频率的 word-piece tokenizer。
    从胶囊文本自动构建 ~3000 token 的词典。
    """
    def __init__(self):
        self.vocab: list[str] = []
        self.stoi: dict[str, int] = {}
        self.itos: dict[int, str] = {}

    @classmethod
    def from_texts(cls, texts: list[str], vocab_size: int = 3000) -> "SimpleTokenizer":
        """从文本语料库构建 tokenizer（中英文混合）"""
        from collections import Counter
        word_freq: Counter[str] = Counter()

        for text in texts:
            # 英文词
            english_words = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', text)
            word_freq.update(w.lower() for w in english_words)
            # 中文：按字符
            chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
            word_freq.update(chinese_chars)
            # 数字和符号
            symbols = re.findall(r'[0-9]+|[^\sa-zA-Z0-9\u4e00-\u9fff]{1,3}', text)
            word_freq.update(s.lower() for s in symbols if len(s) > 0)
            # 2-gram / 3-gram 字符（捕获常用词组）
            for n in (2, 3):
                for i in range(len(text) - n + 1):
                    chunk = text[i:i+n]
                    if not chunk.strip():
                        continue
                    word_freq[chunk] += 1

        # 取最高频的词片
        sorted_words = sorted(word_freq.items(), key=lambda x: -x[1])
        vocab = ["<PAD>", "<UNK>", "<EOS>"] + [w for w, _ in sorted_words[:vocab_size - 3] if len(w) > 0]
        tok = cls()
        tok.vocab = vocab[:vocab_size]
        tok.stoi = {w: i for i, w in enumerate(tok.vocab)}
        tok.itos = {i: w for w, i in tok.stoi.items()}
        return tok

    def encode(self, text: str) -> list[int]:
        """将文本编码为 token id 序列（中英文混合）"""
        ids = []
        english_words = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', text)
        for w in english_words:
            ids.append(self.stoi.get(w.lower(), self.stoi["<UNK>"]))
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
        for c in chinese_chars:
            ids.append(self.stoi.get(c, self.stoi["<UNK>"]))
        ids.append(self.stoi["<EOS>"])
        return ids

    def decode(self, ids: list[int]) -> str:
        """将 token id 序列解码为文本"""
        words = [self.itos.get(i, "<UNK>") for i in ids if i != self.stoi.get("<PAD>", 0)]
        return " ".join(words)

    def save(self, path: Path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"vocab": self.vocab, "stoi": self.stoi, "itos": {str(k): v for k, v in self.itos.items()}}, f)

    @classmethod
    def load(cls, path: Path) -> "SimpleTokenizer":
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        tok = cls()
        tok.vocab = data["vocab"]
        tok.stoi = data["stoi"]
        tok.itos = {int(k): v for k, v in data.get("itos", {}).items()}
        return tok


# ── Dataset ──────────────────────────────────────────────────

class CapsuleDataset(Dataset):
    """将 token 序列转换为 (context, next_token) 训练对"""
    def __init__(self, token_ids: list[int], block_size: int):
        self.token_ids = token_ids
        self.block_size = block_size

    def __len__(self):
        return max(0, len(self.token_ids) - self.block_size)

    def __getitem__(self, idx):
        x = self.token_ids[idx:idx + self.block_size]
        y = self.token_ids[idx + 1:idx + self.block_size + 1]
        return torch.tensor(x, dtype=torch.long), torch.tensor(y, dtype=torch.long)


class TaggedCapsuleDataset(Dataset):
    """
    用于分类头训练的 dataset：返回 (input_ids, tag_targets)。
    tag_targets 是 multi-hot 向量。
    """
    def __init__(self, samples: list[dict], tokenizer: SimpleTokenizer, tag_to_idx: dict[str, int], max_len: int = BLOCK_SIZE):
        self.samples = samples
        self.tokenizer = tokenizer
        self.tag_to_idx = tag_to_idx
        self.max_len = max_len

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        sample = self.samples[idx]
        text = sample["text"][:self.max_len * 4]
        tokens = self.tokenizer.encode(text)[:self.max_len]
        # Pad
        if len(tokens) < self.max_len:
            tokens = tokens + [self.tokenizer.stoi["<PAD>"]] * (self.max_len - len(tokens))
        x = torch.tensor(tokens, dtype=torch.long)
        # Multi-hot tags
        tag_vec = torch.zeros(len(self.tag_to_idx), dtype=torch.float32)
        for tag in sample.get("tags", []):
            if tag in self.tag_to_idx:
                tag_vec[self.tag_to_idx[tag]] = 1.0
        return x, tag_vec


# ── GPT 模型 ────────────────────────────────────────────────

class Head(nn.Module):
    def __init__(self, head_size: int):
        super().__init__()
        self.key = nn.Linear(N_EMBED, head_size, bias=False)
        self.query = nn.Linear(N_EMBED, head_size, bias=False)
        self.value = nn.Linear(N_EMBED, head_size, bias=False)
        self.register_buffer("tril", torch.tril(torch.ones(BLOCK_SIZE, BLOCK_SIZE)))
        self.dropout = nn.Dropout(DROPOUT)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        B, T, C = x.shape
        k = self.key(x)
        q = self.query(x)
        wei = q @ k.transpose(-2, -1) * (C ** -0.5)
        wei = wei.masked_fill(self.tril[:T, :T] == 0, float("-inf"))
        wei = torch.softmax(wei, dim=-1)
        wei = self.dropout(wei)
        v = self.value(x)
        return wei @ v


class MultiHeadAttention(nn.Module):
    def __init__(self, num_heads: int, head_size: int):
        super().__init__()
        self.heads = nn.ModuleList([Head(head_size) for _ in range(num_heads)])
        self.proj = nn.Linear(N_EMBED, N_EMBED, bias=False)
        self.dropout = nn.Dropout(DROPOUT)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out = torch.cat([h(x) for h in self.heads], dim=-1)
        return self.dropout(self.proj(out))


class FeedFwd(nn.Module):
    def __init__(self, n_embed: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_embed, 4 * n_embed),
            nn.GELU(),
            nn.Linear(4 * n_embed, n_embed),
            nn.Dropout(DROPOUT),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class Block(nn.Module):
    def __init__(self, n_embed: int, n_head: int):
        super().__init__()
        head_size = n_embed // n_head
        self.attn = MultiHeadAttention(n_head, head_size)
        self.ffwd = FeedFwd(n_embed)
        self.ln1 = nn.LayerNorm(n_embed)
        self.ln2 = nn.LayerNorm(n_embed)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x + self.attn(self.ln1(x))
        x = x + self.ffwd(self.ln2(x))
        return x


class AmberGPT(nn.Module):
    """
    GPT 模型，架构同 auto-research train.py。
    vocab_size 在实例化时指定。
    可选传入 tag_vocab_size 开启分类头。
    """
    def __init__(self, vocab_size: int, tag_vocab_size: int = 0):
        super().__init__()
        self.vocab_size = vocab_size
        self.tag_vocab_size = tag_vocab_size
        self.token_embedding = nn.Embedding(vocab_size, N_EMBED)
        self.position_embedding = nn.Embedding(BLOCK_SIZE, N_EMBED)
        self.blocks = nn.Sequential(*[Block(N_EMBED, N_HEAD) for _ in range(N_LAYER)])
        self.ln = nn.LayerNorm(N_EMBED)
        self.lm_head = nn.Linear(N_EMBED, vocab_size, bias=False)
        # 权重绑定
        self.lm_head.weight = self.token_embedding.weight

        # ── Enhancement 2: Tag 分类头 ─────────────────────
        if tag_vocab_size > 0:
            self.tag_head = nn.Sequential(
                nn.Linear(N_EMBED, N_EMBED // 2),
                nn.GELU(),
                nn.Dropout(DROPOUT),
                nn.Linear(N_EMBED // 2, tag_vocab_size),
            )
        else:
            self.tag_head = None

    def forward(self, idx: torch.Tensor, targets: torch.Tensor | None = None, return_tags: bool = False):
        B, T = idx.shape
        tok_emb = self.token_embedding(idx)
        pos_emb = self.position_embedding(torch.arange(T, device=idx.device))
        x = tok_emb + pos_emb
        x = self.blocks(x)
        x = self.ln(x)
        logits = self.lm_head(x)

        loss = None
        tag_loss = None
        if targets is not None:
            loss = torch.nn.functional.cross_entropy(
                logits.view(-1, logits.size(-1)), targets.view(-1)
            )

        tag_logits = None
        if self.tag_head is not None and return_tags:
            # 取 last token 的表示预测标签
            tag_logits = self.tag_head(x[:, -1, :])

        return logits, loss, tag_logits, tag_loss

    def forward_lm(self, idx: torch.Tensor, targets: torch.Tensor | None = None):
        """标准语言模型 forward（无 tag）"""
        B, T = idx.shape
        tok_emb = self.token_embedding(idx)
        pos_emb = self.position_embedding(torch.arange(T, device=idx.device))
        x = tok_emb + pos_emb
        x = self.blocks(x)
        x = self.ln(x)
        logits = self.lm_head(x)
        loss = None
        if targets is not None:
            loss = torch.nn.functional.cross_entropy(
                logits.view(-1, logits.size(-1)), targets.view(-1)
            )
        return logits, loss

    @torch.no_grad()
    def encode(self, token_ids: list[int]) -> torch.Tensor:
        """返回 last token 的隐藏状态"""
        self.eval()
        idx = torch.tensor([token_ids[-BLOCK_SIZE:]], dtype=torch.long)
        if idx.device != self.lm_head.weight.device:
            idx = idx.to(self.lm_head.weight.device)
        tok_emb = self.token_embedding(idx)
        pos_emb = self.position_embedding(torch.arange(idx.shape[1], device=idx.device))
        x = tok_emb + pos_emb
        x = self.blocks(x)
        x = self.ln(x)
        return x[0, -1, :]

    @torch.no_grad()
    def generate(self, primer: list[int], max_new: int = 20) -> list[int]:
        """自回归生成"""
        self.eval()
        idx = torch.tensor([primer[-BLOCK_SIZE:]], dtype=torch.long)
        for _ in range(max_new):
            logits, _ = self.forward_lm(idx)
            logits = logits[0, -1, :]
            probs = torch.softmax(logits, dim=-1)
            next_tok = torch.multinomial(probs, 1).item()
            if next_tok == self.token_embedding.weight.shape[0] - 1:
                break
            idx = torch.cat([idx, torch.tensor([[next_tok]])], dim=1)
        return idx[0].tolist()

    @torch.no_grad()
    def predict_tags(self, token_ids: list[int]) -> torch.Tensor:
        """给定 token 序列，预测 tag logits"""
        self.eval()
        idx = torch.tensor([token_ids[:BLOCK_SIZE]], dtype=torch.long)
        if idx.device != self.lm_head.weight.device:
            idx = idx.to(self.lm_head.weight.device)
        tok_emb = self.token_embedding(idx)
        pos_emb = self.position_embedding(torch.arange(idx.shape[1], device=idx.device))
        x = tok_emb + pos_emb
        x = self.blocks(x)
        x = self.ln(x)
        return self.tag_head(x[:, -1, :])


# ── Enhancement 3: GPT-2 预训练初始化 ─────────────────────────

def load_pretrained_gpt2(vocab_size: int, tag_vocab_size: int = 0) -> AmberGPT:
    """
    从 GPT-2 初始化 AmberGPT 权重。
    GPT-2 的 key_proj/query_proj/value_proj/output_proj 映射到我们的 Head 实现。
    """
    from transformers import GPT2Model, GPT2Config
    config = GPT2Config(
        vocab_size=50257,  # GPT-2 BPE vocab
        n_positions=1024,
        n_embd=N_EMBED,
        n_head=N_HEAD,
        n_layer=N_LAYER,
        resid_dropout=DROPOUT,
        embd_dropout=DROPOUT,
    )
    gpt2 = GPT2Model(config)

    model = AmberGPT(vocab_size=vocab_size, tag_vocab_size=tag_vocab_size)

    # 映射 GPT-2 权重 → AmberGPT
    # GPT-2 使用 Conv1D 而我们是 Linear，shape 是 transpose 关系
    with torch.no_grad():
        # token embedding
        model.token_embedding.weight[:50257] = gpt2.wte.weight[:vocab_size]
        # position embedding
        model.position_embedding.weight[:] = gpt2.wpe.weight[:BLOCK_SIZE]

        # transformer blocks
        for i, block in enumerate(model.blocks):
            gpt2_block = gpt2.h[i]
            # attention
            block.attn.heads[0].key.weight[:] = gpt2_block.attn.c_attn.weight[:, :N_EMBED].t()
            block.attn.heads[0].query.weight[:] = gpt2_block.attn.c_attn.weight[:, N_EMBED:N_EMBED*2].t()
            block.attn.heads[0].value.weight[:] = gpt2_block.attn.c_attn.weight[:, N_EMBED*2:].t()
            block.attn.proj.weight[:] = gpt2_block.attn.c_proj.weight.t()
            # ffwd
            block.ffwd.net[0].weight[:] = gpt2_block.mlp.c_fc.weight.t()
            block.ffwd.net[2].weight[:] = gpt2_block.mlp.c_proj.weight.t()
            # layernorm
            block.ln1.weight[:] = gpt2_block.ln_1.weight
            block.ln1.bias[:] = gpt2_block.ln_1.bias
            block.ln2.weight[:] = gpt2_block.ln_2.weight
            block.ln2.bias[:] = gpt2_block.ln_2.bias

        # final layernorm
        model.ln.weight[:] = gpt2.ln_f.weight
        model.ln.bias[:] = gpt2.ln_f.bias

    print(f"[trainer] Initialized AmberGPT from GPT-2 pretrained weights")
    return model


# ── 数据加载 ──────────────────────────────────────────────────

def _load_capsule_texts() -> list[str]:
    """加载所有胶囊的文本内容"""
    import sqlite3
    texts = []
    try:
        DB_PATH = Path.home() / ".amber-hunter" / "hunter.db"
        conn = sqlite3.connect(str(DB_PATH))
        c = conn.cursor()
        last_ts: float | None = None
        batch_size = 300
        while True:
            if last_ts is not None:
                rows = c.execute(
                    "SELECT memo, content, tags, created_at FROM capsules WHERE created_at < ? ORDER BY created_at DESC LIMIT ?",
                    (last_ts, batch_size)
                ).fetchall()
            else:
                rows = c.execute(
                    "SELECT memo, content, tags, created_at FROM capsules ORDER BY created_at DESC LIMIT ?",
                    (batch_size,)
                ).fetchall()
            if not rows:
                break
            for memo, content, tags, created_at in rows:
                if memo:
                    texts.append(memo)
                if content:
                    texts.append(content[:500])
            last_ts = rows[-1][3]
            if len(rows) < batch_size:
                break
        conn.close()
    except Exception as e:
        print(f"[trainer] Failed to load capsules: {e}")
    return texts


def _load_wal_texts() -> list[str]:
    """加载 WAL session 条目文本（Enhancement 1）"""
    texts = []
    WAL_FILE = Path.home() / ".amber-hunter" / "session_wal.jsonl"
    if not WAL_FILE.exists():
        return texts
    try:
        for line in open(WAL_FILE, encoding="utf-8"):
            try:
                entry = json.loads(line)
                text = entry.get("data", {}).get("text", "")[:200]
                if text:
                    texts.append(text)
            except Exception:
                pass
    except Exception as e:
        print(f"[trainer] Failed to load WAL: {e}")
    return texts


def _load_agent_session_texts() -> list[str]:
    """加载 agent session 目录中的对话文本（Enhancement 1）"""
    texts = []
    SESSION_DIR = Path.home() / ".openclaw" / "agents"
    if not SESSION_DIR.exists():
        return texts
    try:
        for transcript_file in SESSION_DIR.rglob("transcript*.jsonl"):
            for line in open(transcript_file, encoding="utf-8"):
                try:
                    entry = json.loads(line)
                    if entry.get("role") == "user":
                        text = entry.get("text", "")[:300]
                        if text:
                            texts.append(text)
                except Exception:
                    pass
    except Exception as e:
        print(f"[trainer] Failed to load agent sessions: {e}")
    return texts


def _is_noise_tag(tag: str) -> bool:
    """判断是否为噪声 tag"""
    import re
    # 太短
    if len(tag) < 2:
        return True
    # 系统生成标签
    if re.match(r"^(related|auto-|signal:|ref:|link:)", tag):
        return True
    # 日期字符串
    if re.match(r"^\d{4}-\d{2}-\d{2}$", tag):
        return True
    # 哈希值
    if re.match(r"^[a-f0-9]{8,}$", tag):
        return True
    # 常见水果/无关名词（需要过滤的噪声）
    NOISE_TAGS = {"loquat", "apple", "banana", "orange", "grape"}
    if tag in NOISE_TAGS:
        return True
    return False


# 中文 ↔ 英文 同义 tag 合并映射
_TAG_CANONICAL: dict[str, str] = {
    "preference": "preference",
    "偏好": "preference",
    "decision": "decision",
    "决策": "decision",
    "fact": "personal_fact",
    "personal_fact": "personal_fact",
    "项目": "project",
    "project": "project",
    "技术": "tech",
    "tech": "tech",
    "error_fix": "error_fix",
    "bug": "error_fix",
    "创意": "creative",
    "creative": "creative",
    "学习": "learning",
    "learning": "learning",
}


def _canonical_tag(tag: str) -> str:
    """将 tag 规范化为标准形式"""
    t = tag.strip().lower()
    if t in _TAG_CANONICAL:
        return _TAG_CANONICAL[t]
    return t


def _build_tag_vocab() -> tuple[dict[str, int], list[dict]]:
    """
    从胶囊 tags 构建标签词汇表和分类训练样本。
    返回 (tag_to_idx, training_samples)
    包含降噪：过滤系统标签、日期、哈希值、常见噪声词，合并中英同义 tag。
    """
    import sqlite3
    from collections import Counter
    tag_freq: Counter[str] = Counter()

    samples: list[dict] = []
    try:
        DB_PATH = Path.home() / ".amber-hunter" / "hunter.db"
        conn = sqlite3.connect(str(DB_PATH))
        c = conn.cursor()
        rows = c.execute(
            "SELECT memo, tags FROM capsules WHERE tags IS NOT NULL AND tags != '' LIMIT 2000"
        ).fetchall()
        for memo, tags in rows:
            if not tags or not memo:
                continue
            raw_tags = [t.strip().lower() for t in tags.split(",") if t.strip()]
            # 降噪 + 规范化
            tag_list = []
            for t in raw_tags:
                if _is_noise_tag(t):
                    continue
                canon = _canonical_tag(t)
                tag_list.append(canon)
                tag_freq[canon] += 1
            if tag_list:
                samples.append({"text": memo, "tags": tag_list})
        conn.close()
    except Exception as e:
        print(f"[trainer] Failed to build tag vocab: {e}")

    # 取最高频的 TAG_VOCAB_SIZE 个标签（按规范化后的频率）
    common_tags = [t for t, _ in tag_freq.most_common(TAG_VOCAB_SIZE)]
    tag_to_idx = {t: i for i, t in enumerate(common_tags)}

    # 保存
    TAG_VOCAB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(TAG_VOCAB_PATH, "w", encoding="utf-8") as f:
        json.dump({"tag_to_idx": tag_to_idx, "idx_to_tag": {i: t for t, i in tag_to_idx.items()}}, f)

    print(f"[trainer] Tag vocab: {len(tag_to_idx)} tags (denoised), {len(samples)} labeled samples")
    return tag_to_idx, samples


# ── 训练 ─────────────────────────────────────────────────────

def fine_tune(
    vocab_size: int = 2500,
    iterations: int = MAX_ITERS,
    lr: float = LEARNING_RATE,
    batch_size: int = 32,
    device: str | None = None,
    use_gpt2_pretrain: bool = True,
    incremental: bool = True,
    progress_callback=None,
) -> dict:
    """
    在用户胶囊数据上 fine-tune AmberGPT。
    Enhancement 3: 支持 GPT-2 预训练初始化
    Enhancement 4: 支持从已有 checkpoint 继续训练
    返回 {"status": "ok", "iterations": int, "final_loss": float, "model_path": str}
    """
    torch.manual_seed(42)
    np.random.seed(42)

    if device is None:
        if torch.backends.mps.is_available():
            device = "mps"
        elif torch.cuda.is_available():
            device = "cuda"
        else:
            device = "cpu"
    print(f"[trainer] Using device: {device}")

    # Enhancement 4: 提前加载 checkpoint 元数据（仅 tag_vocab_size）
    ckpt_tag_vocab_size = 0
    ckpt_vocab_size = None
    if incremental and MODEL_PATH.exists():
        try:
            ckpt = torch.load(MODEL_PATH, map_location=device, weights_only=False)
            ckpt_tag_vocab_size = ckpt.get("tag_vocab_size", 0)
            ckpt_vocab_size = ckpt.get("vocab_size")
            print(f"[trainer] Found checkpoint: vocab={ckpt_vocab_size}, tag_vocab={ckpt_tag_vocab_size}")
        except Exception:
            pass

    # 1. 加载所有训练文本
    print("[trainer] Loading training data...")
    capsule_texts = _load_capsule_texts()
    wal_texts = _load_wal_texts()
    agent_texts = _load_agent_session_texts()
    all_texts = capsule_texts + wal_texts + agent_texts
    print(f"[trainer] Data: {len(capsule_texts)} capsules, {len(wal_texts)} WAL, {len(agent_texts)} agent sessions")

    if len(all_texts) < 50:
        return {"status": "error", "error": "Not enough training data"}

    # 2. 构建 tokenizer
    print("[trainer] Building tokenizer...")
    tokenizer = SimpleTokenizer.from_texts(all_texts, vocab_size=vocab_size)
    tokenizer.save(TOKENIZER_PATH)
    print(f"[trainer] Vocab size: {len(tokenizer.vocab)}")

    # 3. 构建训练 token 序列
    print("[trainer] Building training tokens...")
    all_tokens: list[int] = []
    for text in all_texts:
        all_tokens.extend(tokenizer.encode(text))
    print(f"[trainer] Total tokens: {len(all_tokens)}")

    if len(all_tokens) < BLOCK_SIZE * 10:
        return {"status": "error", "error": f"Only {len(all_tokens)} tokens, need more data"}

    # 4. 构建 tag vocab 和分类样本（Enhancement 2）
    # 如果 checkpoint 已有 tag vocab，保留它；否则用新构建的
    tag_to_idx: dict[str, int] = {}
    tag_samples: list[dict] = []
    new_tag_vocab_size = 0
    if incremental:
        tag_to_idx, tag_samples = _build_tag_vocab()
        new_tag_vocab_size = len(tag_to_idx)
    # 保留 checkpoint 的 tag vocab（更大），否则用新的
    tag_vocab_size = max(ckpt_tag_vocab_size, new_tag_vocab_size)
    if tag_vocab_size < 5:
        tag_vocab_size = 0  # 标签太少，禁用分类头

    # 5. 分割训练/验证
    split = int(len(all_tokens) * 0.9)
    train_tokens = all_tokens[:split]
    val_tokens = all_tokens[split:]

    train_ds = CapsuleDataset(train_tokens, BLOCK_SIZE)
    val_ds = CapsuleDataset(val_tokens, BLOCK_SIZE)
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)

    # 6. 模型初始化
    # Enhancement 4: 尝试从 checkpoint 继续
    start_iter = 0
    if incremental and MODEL_PATH.exists():
        try:
            ckpt = torch.load(MODEL_PATH, map_location=device, weights_only=False)
            ckpt_tag_vocab_size = ckpt.get("tag_vocab_size", 0)
            model = AmberGPT(vocab_size=ckpt["vocab_size"], tag_vocab_size=ckpt_tag_vocab_size)
            model.load_state_dict(ckpt["model_state"], strict=False)
            start_iter = ckpt.get("iterations", 0)
            print(f"[trainer] Resumed from checkpoint (iter {start_iter})")
        except Exception as e:
            print(f"[trainer] Could not resume checkpoint: {e}, starting fresh")
            model = None
    else:
        model = None

    if model is None:
        if use_gpt2_pretrain:
            try:
                model = load_pretrained_gpt2(vocab_size=len(tokenizer.vocab), tag_vocab_size=tag_vocab_size)
            except Exception as e:
                print(f"[trainer] GPT-2 init failed ({e}), training from scratch")
                model = AmberGPT(vocab_size=len(tokenizer.vocab), tag_vocab_size=tag_vocab_size)
        else:
            model = AmberGPT(vocab_size=len(tokenizer.vocab), tag_vocab_size=tag_vocab_size)

    model.to(device)
    optimizer = optim.AdamW(model.parameters(), lr=lr, weight_decay=WEIGHT_DECAY)

    print(f"[trainer] Model params: {sum(p.numel() for p in model.parameters()):,}")
    print(f"[trainer] Tag vocab: {tag_vocab_size} tags")

    # 7. 训练循环
    model.train()
    start_time = time.time()
    best_val_loss = float("inf")

    iter_count = start_iter
    final_loss = 0.0

    while iter_count < start_iter + iterations:
        epoch_start = time.time()
        for xb, yb in train_loader:
            if time.time() - start_time > 300:  # 5分钟 wall clock 保护
                break

            xb, yb = xb.to(device), yb.to(device)
            _, loss = model.forward_lm(xb, yb)
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()

            iter_count += 1
            if progress_callback:
                progress_callback(iter_count, loss.item())

            if iter_count >= start_iter + iterations:
                break

        # 验证
        model.eval()
        val_loss = 0.0
        count = 0
        with torch.no_grad():
            for xb, yb in val_loader:
                xb, yb = xb.to(device), yb.to(device)
                _, loss = model.forward_lm(xb, yb)
                val_loss += loss.item()
                count += 1
        val_loss /= max(count, 1)
        model.train()

        elapsed = time.time() - epoch_start
        bpb = val_loss / math.log(2)
        print(f"[trainer] iter {iter_count:4d} | val_loss: {val_loss:.4f} | val_bpb: {bpb:.4f} | elapsed: {elapsed:.1f}s")

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save({
                "model_state": model.state_dict(),
                "vocab_size": len(tokenizer.vocab),
                "tag_vocab_size": tag_vocab_size,
                "iterations": iter_count,
                "val_loss": best_val_loss,
            }, MODEL_PATH)

        final_loss = val_loss

    elapsed = time.time() - start_time
    print(f"[trainer] Training complete in {elapsed:.1f}s, best val_loss: {best_val_loss:.4f}")

    return {
        "status": "ok",
        "iterations": iter_count,
        "final_loss": final_loss,
        "val_bpb": final_loss / math.log(2),
        "model_path": str(MODEL_PATH),
        "tokenizer_path": str(TOKENIZER_PATH),
        "tag_vocab_size": tag_vocab_size,
        "device": device,
    }


# ── 推理 API ─────────────────────────────────────────────────

class AmberTrainer:
    """
    加载训练好的模型，提供推理 API。
    """
    _instance: Optional["AmberTrainer"] = None

    def __init__(self):
        self.model: AmberGPT | None = None
        self.tokenizer: SimpleTokenizer | None = None
        self.tag_to_idx: dict[str, int] = {}
        self.idx_to_tag: dict[int, str] = {}
        self.device: str = "cpu"
        self._load()

    def _load(self):
        if not MODEL_PATH.exists() or not TOKENIZER_PATH.exists():
            return
        try:
            self.tokenizer = SimpleTokenizer.load(TOKENIZER_PATH)
            ckpt = torch.load(MODEL_PATH, map_location="cpu", weights_only=False)
            tag_vocab_size = ckpt.get("tag_vocab_size", 0)
            self.model = AmberGPT(vocab_size=ckpt["vocab_size"], tag_vocab_size=tag_vocab_size)
            self.model.load_state_dict(ckpt["model_state"], strict=False)

            # 加载 tag vocab
            if TAG_VOCAB_PATH.exists():
                with open(TAG_VOCAB_PATH, encoding="utf-8") as f:
                    tag_data = json.load(f)
                    self.tag_to_idx = tag_data.get("tag_to_idx", {})
                    self.idx_to_tag = {int(k): v for k, v in tag_data.get("idx_to_tag", {}).items()}

            if torch.backends.mps.is_available():
                self.device = "mps"
                self.model.to("mps")
            print(f"[trainer] Loaded model from {MODEL_PATH}")
        except Exception as e:
            print(f"[trainer] Failed to load model: {e}")
            self.model = None

    def is_ready(self) -> bool:
        return self.model is not None and self.tokenizer is not None

    def has_tag_head(self) -> bool:
        return self.is_ready() and self.model is not None and self.model.tag_head is not None

    @torch.no_grad()
    def score(self, query: str, memory_text: str) -> float:
        """给定 query 和 memory 文本，返回相关度分数 [0, 1]"""
        if not self.is_ready():
            return 0.5
        q_tokens = self.tokenizer.encode(query)[:BLOCK_SIZE // 2]
        m_tokens = self.tokenizer.encode(memory_text)[:BLOCK_SIZE // 2]
        q_emb = self.model.encode(q_tokens)
        m_emb = self.model.encode(m_tokens)
        sim = torch.nn.functional.cosine_similarity(
            q_emb.unsqueeze(0), m_emb.unsqueeze(0)
        ).item()
        return float(max(0.0, min(1.0, sim)))

    @torch.no_grad()
    def rerank(self, query: str, memory_texts: list[str], top_k: int = 5) -> list[tuple[int, float]]:
        """对 memory 列表 rerank，返回 [(index, score), ...]"""
        if not self.is_ready():
            return [(i, 0.5) for i in range(len(memory_texts))]
        scores = [self.score(query, mem) for mem in memory_texts]
        return sorted(enumerate(scores), key=lambda x: -x[1])[:top_k]

    @torch.no_grad()
    def predict_tags(self, text: str, top_k: int = 3) -> list[tuple[str, float]]:
        """
        Enhancement 2: 预测 text 的标签，返回 [(tag, score), ...]。
        需要训练时开启分类头。
        """
        if not self.has_tag_head():
            return []
        tokens = self.tokenizer.encode(text)[:BLOCK_SIZE]
        logits = self.model.predict_tags(tokens)
        probs = torch.sigmoid(logits).cpu().flatten()  # (1, tag_vocab) -> (tag_vocab,)
        # 取 top-k
        k = min(top_k, len(probs))
        top_indices = torch.topk(probs, k).indices.tolist()
        return [(self.idx_to_tag.get(i, "?"), float(probs[i])) for i in top_indices]

    @torch.no_grad()
    def extract_memories(self, conversation: str, max_new_tokens: int = 50) -> list[str]:
        """给定对话文本，用模型生成记忆片段"""
        if not self.is_ready():
            return []
        primer = self.tokenizer.encode(conversation[:BLOCK_SIZE])
        generated_ids = self.model.generate(primer, max_new=max_new_tokens)
        generated_text = self.tokenizer.decode(generated_ids[len(primer):])
        sentences = re.split(r'[。.!]+', generated_text)
        return [s.strip() for s in sentences if len(s.strip()) > 10]


# ── 单例访问 ─────────────────────────────────────────────────

def get_trainer() -> AmberTrainer:
    if AmberTrainer._instance is None:
        AmberTrainer._instance = AmberTrainer()
    return AmberTrainer._instance


def is_trained() -> bool:
    """检查是否有已训练的模型"""
    return MODEL_PATH.exists() and TOKENIZER_PATH.exists()


# ── CLI ──────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AmberGPT Fine-tune & Inference")
    parser.add_argument("action", choices=["train", "score", "rerank", "status", "tags"])
    parser.add_argument("--query", type=str, default="")
    parser.add_argument("--memory", type=str, default="")
    parser.add_argument("--text", type=str, default="")
    args = parser.parse_args()

    if args.action == "train":
        print(f"[trainer] Starting fine-tune...")
        result = fine_tune()
        print(json.dumps(result, indent=2))

    elif args.action == "score":
        at = get_trainer()
        if not at.is_ready():
            print("Model not trained yet."); sys.exit(1)
        print(f"Relevance: {at.score(args.query, args.memory):.4f}")

    elif args.action == "rerank":
        at = get_trainer()
        if not at.is_ready():
            print("Not trained."); sys.exit(1)
        memories = args.memory.split("|")
        for idx, score in at.rerank(args.query, memories):
            print(f"[{score:.3f}] {memories[idx][:80]}")

    elif args.action == "tags":
        at = get_trainer()
        if not at.has_tag_head():
            print("Tag head not available (needs training with --train-tags)")
            sys.exit(1)
        tags = at.predict_tags(args.text)
        for tag, score in tags:
            print(f"[{score:.3f}] {tag}")

    elif args.action == "status":
        if is_trained():
            ckpt = torch.load(MODEL_PATH, map_location="cpu", weights_only=False)
            print(f"Model: {MODEL_PATH}")
            print(f"  iterations: {ckpt.get('iterations', '?')}")
            print(f"  val_loss: {ckpt.get('val_loss', '?'):.4f}")
            print(f"  vocab_size: {ckpt.get('vocab_size', '?')}")
            print(f"  tag_vocab_size: {ckpt.get('tag_vocab_size', 0)}")
        else:
            print("No trained model yet.")
