# Amber-Hunter 开发准则

> 完整项目文档: `/Users/leo/Documents/个人AI项目/Huper/README.md`

## 仓库结构

| 目录 | 用途 |
|------|------|
| `/Users/leo/Documents/个人AI项目/Huper/amber-hunter/` | **开发 git 仓库**（本目录） |
| `~/.openclaw/skills/amber-hunter/` | **OpenClaw 运行时目录**，由本仓库 sync-to-runtime.sh 同步 |
| GitHub | `github.com/ankechenlab-node/amber_hunter`（公开） |
| ClawHub | 自动从 GitHub 同步 |

## 开发流程

```
开发 → git commit
       ↓ ./sync-to-runtime.sh
~/.openclaw/skills/amber-hunter/ （OpenClaw 实际运行）
       ↓ ./release.sh + git push
GitHub → ClawHub → 用户安装
```

### 同步到运行时
```bash
./sync-to-runtime.sh
# 或手动：
rsync -av \
  --exclude='.git' --exclude='.synapse' --exclude='.knowledge' \
  --exclude='memory.db' --exclude='*.lance/' \
  /Users/leo/Documents/个人AI项目/Huper/amber-hunter/ \
  ~/.openclaw/skills/amber-hunter/
```

### 发布流程
```bash
./release.sh  # 自动更新版本号 + CHANGELOG + SKILL.md + git tag
git push origin main --tags
```

## 版本规范

- 格式：`X.Y.Z`
- **Z**：每次迭代递增（v1.2.41 → v1.2.42）
- **Y**：需明确指令才递增
- **递增后必须更新**（见 RELEASE_CHECKLIST.md）：
  1. `amber_hunter.py`（4处版本号）
  2. `SKILL.md`（header + API Endpoints 小节）
  3. `CHANGELOG.md`（TOP 新增 entry）

## 安全规范（发布前必查）

```bash
grep -r "ghp_\|sk-\|YOUR_KEY\|api_key.*=" . --include="*.py" --include="*.sh"
grep -r "anKe\|ankechen\|/Users/leo" . --include="*.py" --include="*.sh"
```

- `master_password` → macOS Keychain
- `api_token` → `~/.amber-hunter/config.json`

## Amber-Pipeline（强制）

所有非琐碎开发必须走 SOP 流水线：

```bash
cd /Users/leo/pipeline-workspace
python3 pipeline.py run-pipeline amber-hunter \
  --input "需求描述" \
  --verbose
```

流程：REQ → ARCH（签合约）→ DEV → INT → QA（真实对抗测试）→ DEPLOY

禁止直接 patch / scp 部署绕过流水线。

## OpenClaw 重启

```bash
launchctl unload ~/Library/LaunchAgents/com.huper.amber-hunter.plist
launchctl load ~/Library/LaunchAgents/com.huper.amber-hunter.plist
```

## 测试

```bash
python3 -m pytest tests/ -v
# 当前: 44 passed, 1 failed (test_notify_returns_ok_on_success)
```

## 核心模块说明

| 模块 | 用途 |
|------|------|
| `core/db.py` | SQLite 数据库 |
| `core/vector.py` | LanceDB 向量索引 |
| `core/embedding.py` | BGE-M3 1024维向量化 |
| `core/reranker.py` | Cross-Encoder Reranker |
| `core/bm25.py` | BM25 关键词检索 |
| `core/hyde.py` | HyDE 假设性答案 |
| `core/crypto.py` | AES-256-GCM 加密 |
| `core/keychain.py` | macOS Keychain 集成 |
| `core/llm.py` | MiniMax/OpenAI/Ollama LLM 调用 |
| `core/extractor.py` | Mem0 LLM 自动抽取 |
| `core/profile.py` | Structured User Profile |
| `core/session.py` | Session 管理 + WAL |
| `core/contradiction.py` | 矛盾检测 |
| `core/correction.py` | Self-Correction Loop |
| `core/wiki_compiler.py` | Wiki 知识编译器 |

## 端点快速参考

- `GET /status` — 无认证，服务状态
- `GET /recall?q=` — Bearer Token，混合检索
- `POST /sync` — Bearer Token，推送到云端
- `POST /ingest` — Bearer Token，LLM 自动抽取
- `POST /did/encrypt` — Bearer Token，DID 加密

完整端点列表（74个）见 `/Users/leo/Documents/个人AI项目/Huper/README.md`
