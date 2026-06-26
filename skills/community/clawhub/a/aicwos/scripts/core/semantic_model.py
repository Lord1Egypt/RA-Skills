"""
语义模型管理器 - 下载、加载和推理 ONNX 语义向量模型

基于 text2vec-base-chinese (chinese-macbert-base + CoSENT)
内置轻量级 BERT 分词器，无需 transformers 依赖

配置驱动：所有下载地址和路径拼接规则来自 assets/model/setting.json
模型策略：优先 INT8 量化版(~98MB)，不可用时降级 FP32(~203MB)
下载优先级：HF-Mirror → 腾讯云COS → HuggingFace → huggingface_hub(兜底)
"""

import gc
import json
import struct
import sys
import time
import unicodedata
from pathlib import Path
from typing import Dict, List, Optional

# 技能根目录（scripts/core/ → scripts/ → 技能根）
SKILL_ROOT = Path(__file__).resolve().parent.parent.parent
MODEL_DIR = SKILL_ROOT / "assets" / "model"
SETTING_PATH = MODEL_DIR / "setting.json"


def _load_setting() -> dict:
    """加载 setting.json 配置"""
    if SETTING_PATH.exists():
        return json.loads(SETTING_PATH.read_text(encoding="utf-8"))
    return {}


# 兼容常量（从 setting.json 读取，供其他模块 import）
EMBEDDING_DIM = 768  # 默认值，下面由 setting 覆盖


# 延迟加载配置（仅首次访问时读取）
_SETTING = None


def _get_setting() -> dict:
    global _SETTING, EMBEDDING_DIM
    if _SETTING is None:
        _SETTING = _load_setting()
        EMBEDDING_DIM = _SETTING.get("embedding_dim", 768)
    return _SETTING


# 模块加载时初始化 EMBEDDING_DIM
_get_setting()

# ==================== 轻量级 BERT 分词器 ====================

class BasicTokenizer:
    """基础分词器 - 处理空白符、CJK 字符拆分、标点符号"""

    def __init__(self, do_lower_case: bool = True):
        self.do_lower_case = do_lower_case

    def tokenize(self, text: str) -> List[str]:
        text = self._clean_text(text)
        text = self._tokenize_chinese_chars(text)
        orig_tokens = text.strip().split()
        if self.do_lower_case:
            orig_tokens = [t.lower() for t in orig_tokens]
        tokens = []
        for token in orig_tokens:
            token = self._run_strip_accents(token)
            tokens.extend(self._run_split_on_punctuation(token))
        return " ".join(tokens).strip().split()

    def _clean_text(self, text: str) -> str:
        output = []
        for ch in text:
            cp = ord(ch)
            if cp == 0 or cp == 0xFFFD or self._is_control(ch):
                continue
            if self._is_whitespace(ch):
                output.append(" ")
            else:
                output.append(ch)
        return "".join(output)

    def _tokenize_chinese_chars(self, text: str) -> str:
        output = []
        for ch in text:
            cp = ord(ch)
            if self._is_chinese_char(cp):
                output.append(" ")
                output.append(ch)
                output.append(" ")
            else:
                output.append(ch)
        return "".join(output)

    @staticmethod
    def _is_chinese_char(cp: int) -> bool:
        return ((0x4E00 <= cp <= 0x9FFF) or
                (0x3400 <= cp <= 0x4DBF) or
                (0x20000 <= cp <= 0x2A6DF) or
                (0x2A700 <= cp <= 0x2B73F) or
                (0x2B740 <= cp <= 0x2B81F) or
                (0x2B820 <= cp <= 0x2CEAF) or
                (0xF900 <= cp <= 0xFAFF) or
                (0x2F800 <= cp <= 0x2FA1F))

    def _run_strip_accents(self, text: str) -> str:
        text = unicodedata.normalize("NFD", text)
        output = []
        for ch in text:
            cat = unicodedata.category(ch)
            if cat == "Mn":
                continue
            output.append(ch)
        return "".join(output)

    def _run_split_on_punctuation(self, text: str) -> List[str]:
        tokens = []
        start_new = True
        for ch in text:
            if self._is_punctuation(ch):
                tokens.append([ch])
                start_new = True
            else:
                if start_new:
                    tokens.append([])
                    start_new = False
                tokens[-1].append(ch)
        return ["".join(t) for t in tokens]

    @staticmethod
    def _is_punctuation(ch: str) -> bool:
        cp = ord(ch)
        if (33 <= cp <= 47) or (58 <= cp <= 64) or (91 <= cp <= 96) or (123 <= cp <= 126):
            return True
        cat = unicodedata.category(ch)
        return cat.startswith("P")

    @staticmethod
    def _is_whitespace(ch: str) -> bool:
        if ch in (" ", "\t", "\n", "\r"):
            return True
        cat = unicodedata.category(ch)
        return cat == "Zs"

    @staticmethod
    def _is_control(ch: str) -> bool:
        if ch in ("\t", "\n", "\r"):
            return False
        cat = unicodedata.category(ch)
        return cat.startswith("C")


class WordPieceTokenizer:
    """WordPiece 子词分词器"""

    def __init__(self, vocab: Dict[str, int], unk_token: str = "[UNK]",
                 max_input_chars_per_word: int = 200):
        self.vocab = vocab
        self.unk_token = unk_token
        self.max_input_chars_per_word = max_input_chars_per_word

    def tokenize(self, text: str) -> List[str]:
        output_tokens = []
        for token in text.strip().split():
            chars = list(token)
            if len(chars) > self.max_input_chars_per_word:
                output_tokens.append(self.unk_token)
                continue
            is_bad = False
            start = 0
            sub_tokens = []
            while start < len(chars):
                end = len(chars)
                cur_substr = None
                while start < end:
                    substr = "".join(chars[start:end])
                    if start > 0:
                        substr = "##" + substr
                    if substr in self.vocab:
                        cur_substr = substr
                        break
                    end -= 1
                if cur_substr is None:
                    is_bad = True
                    break
                sub_tokens.append(cur_substr)
                start = end
            if is_bad:
                output_tokens.append(self.unk_token)
            else:
                output_tokens.extend(sub_tokens)
        return output_tokens


class BertTokenizer:
    """轻量级 BERT 分词器 - 无需 transformers 依赖"""

    def __init__(self, vocab_file: str, do_lower_case: bool = True):
        self.vocab = self._load_vocab(vocab_file)
        self.ids_to_tokens = {v: k for k, v in self.vocab.items()}
        self.basic_tokenizer = BasicTokenizer(do_lower_case=do_lower_case)
        self.wordpiece_tokenizer = WordPieceTokenizer(self.vocab)

    @staticmethod
    def _load_vocab(vocab_file: str) -> Dict[str, int]:
        vocab = {}
        with open(vocab_file, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f):
                token = line.strip()
                vocab[token] = idx
        return vocab

    def tokenize(self, text: str) -> List[str]:
        basic_tokens = self.basic_tokenizer.tokenize(text)
        wp_tokens = []
        for token in basic_tokens:
            wp_tokens.extend(self.wordpiece_tokenizer.tokenize(token))
        return wp_tokens

    def convert_tokens_to_ids(self, tokens: List[str]) -> List[int]:
        return [self.vocab.get(t, self.vocab.get("[UNK]", 0)) for t in tokens]

    def __call__(self, text: str, padding: bool = True, truncation: bool = True,
                 max_length: int = 128, return_tensors: str = "np") -> dict:
        import numpy as np
        tokens = ["[CLS]"] + self.tokenize(text)[:max_length - 2] + ["[SEP]"]
        input_ids = self.convert_tokens_to_ids(tokens)
        if padding:
            pad_len = max_length - len(input_ids)
            attention_mask = [1] * len(input_ids) + [0] * pad_len
            input_ids = input_ids + [0] * pad_len
            token_type_ids = [0] * max_length
        else:
            attention_mask = [1] * len(input_ids)
            token_type_ids = [0] * len(input_ids)
        return {
            "input_ids": np.array([input_ids], dtype=np.int64),
            "attention_mask": np.array([attention_mask], dtype=np.int64),
            "token_type_ids": np.array([token_type_ids], dtype=np.int64),
        }


# ==================== 模型下载（配置驱动） ====================

def check_model_files() -> dict:
    """检查模型文件是否就绪"""
    setting = _get_setting()
    files = setting.get("files", [])

    model_ok = False
    active = None

    for f in files:
        if f["id"] == "model":
            path = MODEL_DIR / f["local_name"]
            model_ok = path.exists() and path.stat().st_size > 1000
            if model_ok:
                active = f["local_name"]

    # vocab/config 为预置文件，始终存在
    return {
        "model_ready": model_ok,
        "active_model": active,
        "vocab_ready": (MODEL_DIR / "vocab.txt").exists(),
        "config_ready": (MODEL_DIR / "config.json").exists(),
    }


def _download_file(url: str, dest: Path, desc: str = "") -> bool:
    """通用文件下载"""
    try:
        import urllib.request
        import shutil
        if desc:
            print(f"正在下载 {desc}...", file=sys.stderr)
        dest.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = dest.with_suffix(dest.suffix + ".tmp")
        try:
            with urllib.request.urlopen(url, timeout=300) as resp:
                total = resp.headers.get("Content-Length")
                if total:
                    total = int(total)
                    print(f"  文件大小: {total / 1024 / 1024:.1f}MB", file=sys.stderr)
                with open(tmp_path, "wb") as f:
                    shutil.copyfileobj(resp, f)
            tmp_path.rename(dest)
            return True
        except Exception:
            if tmp_path.exists():
                tmp_path.unlink()
            raise
    except Exception as e:
        print(f"WARNING: 下载失败 [{url}]: {e}", file=sys.stderr)
        return False


def _download_one_file(candidate: str, local_name: str, desc: str = "") -> bool:
    """
    从多个源下载一个文件

    candidate: HuggingFace 仓库内路径（如 onnx/model_qint8_avx512_vnni.onnx）
    local_name: 本地文件名 & COS 路径（如 model_qint8_avx512_vnni.onnx）
    """
    setting = _get_setting()
    sources = setting.get("sources", [])
    dest = MODEL_DIR / local_name

    # 按源优先级逐个尝试
    for src in sources:
        path_type = src.get("path_type", "repo")
        path = candidate if path_type == "repo" else local_name
        url = f"{src['base_url']}/{path}"
        if _download_file(url, dest, f"{desc} ({src['name']})"):
            return True

    # 兜底：huggingface_hub SDK
    fb = setting.get("fallback", {})
    if fb.get("method") == "huggingface_hub":
        try:
            from huggingface_hub import hf_hub_download
            downloaded = hf_hub_download(
                fb["repo"], candidate,
                local_dir=str(MODEL_DIR), local_dir_use_symlinks=False,
            )
            dp = Path(downloaded)
            if dp != dest and dp.exists():
                import shutil
                shutil.move(str(dp), str(dest))
            return True
        except ImportError:
            pass
        except Exception as e:
            print(f"WARNING: huggingface_hub下载失败: {e}", file=sys.stderr)

    return False


def download_model(force: bool = False) -> dict:
    """
    下载模型文件（仅模型，vocab/config已内置）

    下载优先级（由 setting.json 的 sources 顺序决定）：
      HF-Mirror(repo路径) → 腾讯云COS(平铺路径) → HuggingFace(repo路径) → huggingface_hub(兜底)

    仅支持 model_qint8_avx512_vnni.onnx (INT8)，不提供FP32降级方案。
    """
    setting = _get_setting()
    files = setting.get("files", [])
    results = {"downloaded": [], "skipped": [], "errors": []}

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    # 下载模型文件（setting.json files 列表）
    for f in files:
        local_name = f["local_name"]
        dest = MODEL_DIR / local_name
        if dest.exists() and dest.stat().st_size > 1000 and not force:
            results["skipped"].append(local_name)
        else:
            if _download_one_file(f["candidate"], local_name, f.get("desc", local_name)):
                results["downloaded"].append(local_name)
            else:
                results["errors"].append(f"{local_name} 所有下载源均失败")

    return results


# ==================== 语义模型 ====================

class SemanticModel:
    """ONNX 语义模型（仅支持INT8量化模型）"""

    def __init__(self):
        self.session = None
        self.tokenizer = None
        self._mode = "none"
        self._model_file = None

    def load(self) -> str:
        """
        加载模型，返回 'onnx' 或 'fallback'

        仅加载 model_qint8_avx512_vnni.onnx
        """
        setting = _get_setting()
        files = setting.get("files", [])

        # 按优先级查找模型文件
        model_candidates = []
        for f in files:
            if f["id"] == "model":
                model_candidates.append(MODEL_DIR / f["local_name"])

        # 找到 vocab 路径（预置文件）
        vocab_path = MODEL_DIR / "vocab.txt"

        for model_path in model_candidates:
            if not model_path.exists() or model_path.stat().st_size < 1000:
                continue
            try:
                import onnxruntime as ort
                opts = ort.SessionOptions()
                opts.intra_op_num_threads = 2
                opts.inter_op_num_threads = 1
                opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
                self.session = ort.InferenceSession(
                    str(model_path), sess_options=opts,
                    providers=["CPUExecutionProvider"],
                )
                if vocab_path and vocab_path.exists():
                    self.tokenizer = BertTokenizer(str(vocab_path))
                else:
                    print("WARNING: vocab.txt 不存在", file=sys.stderr)
                    self.tokenizer = None
                self._mode = "onnx"
                self._model_file = model_path.name
                return "onnx"
            except ImportError:
                break
            except Exception as e:
                print(f"WARNING: {model_path.name}加载失败: {e}", file=sys.stderr)
                continue

        self._mode = "fallback"
        print("WARNING: 语义模型不可用，向量检索已禁用。运行 db_init.py --download-model 下载模型",
              file=sys.stderr)
        return "fallback"

    @property
    def mode(self) -> str:
        return self._mode

    @property
    def is_available(self) -> bool:
        return self._mode == "onnx"

    @property
    def model_file(self) -> Optional[str]:
        """当前加载的模型文件名"""
        return self._model_file

    def encode(self, text: str) -> List[float]:
        if self._mode != "onnx" or not self.session or not self.tokenizer:
            return []
        try:
            return self._infer(text)
        except Exception as e:
            print(f"WARNING: 编码失败: {e}", file=sys.stderr)
            return []

    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        return [self.encode(t) for t in texts]

    def _infer(self, text: str) -> List[float]:
        setting = _get_setting()
        max_len = setting.get("max_seq_length", 128)
        import numpy as np
        inputs = self.tokenizer(
            text, padding=True, truncation=True,
            max_length=max_len, return_tensors="np",
        )
        feed = {"input_ids": inputs["input_ids"].astype(np.int64),
                "attention_mask": inputs["attention_mask"].astype(np.int64)}
        if "token_type_ids" in inputs:
            feed["token_type_ids"] = inputs["token_type_ids"].astype(np.int64)
        outputs = self.session.run(None, feed)
        token_emb = outputs[0]
        mask = inputs["attention_mask"][:, :, np.newaxis].astype(np.float32)
        summed = np.sum(token_emb * mask, axis=1)
        count = np.clip(mask.sum(axis=1), a_min=1e-9, a_max=None)
        return (summed / count).squeeze().tolist()


# ==================== 向量序列化 ====================

def serialize_vector(vec: List[float]) -> bytes:
    return struct.pack(f"{len(vec)}f", *vec)


def deserialize_vector(blob: bytes, dim: int = None) -> List[float]:
    if dim is None:
        dim = _get_setting().get("embedding_dim", 768)
    return list(struct.unpack(f"{dim}f", blob))


def cosine_similarity(a: List[float], b: List[float]) -> float:
    import numpy as np
    va, vb = np.array(a, dtype=np.float32), np.array(b, dtype=np.float32)
    na, nb = np.linalg.norm(va), np.linalg.norm(vb)
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(va, vb) / (na * nb))


# ==================== CLI 入口 ====================

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="语义模型管理")
    parser.add_argument("--download-model", action="store_true", help="下载ONNX语义模型（优先INT8量化版）")
    parser.add_argument("--force", action="store_true", help="强制重新下载")
    parser.add_argument("--check", action="store_true", help="检查模型状态")
    args = parser.parse_args()

    if args.check:
        print(json.dumps(check_model_files(), ensure_ascii=False, indent=2))
    elif args.download_model:
        print(json.dumps(download_model(force=args.force), ensure_ascii=False, indent=2))
    else:
        parser.print_help()
