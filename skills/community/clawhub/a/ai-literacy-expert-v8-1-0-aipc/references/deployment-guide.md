# V7 部署指南 · ai-literacy-expert-v7 端云协同版

> **版本**：v7.0.0
> **生成时间**：2026-08-15
> **适用场景**：K12 学校、高校、企业培训、教育部门部署 AI PC 教学系统
> **设计哲学**：「端侧重计算 + 云端轻决策」

---

## 📋 文档导航

| 章节 | 内容 | 预计阅读 |
|------|------|----------|
| 第 1 章 | 部署前准备（环境/硬件/网络） | 10 分钟 |
| 第 2 章 | 4 种部署方式对比与选择 | 10 分钟 |
| 第 3 章 | 方式 A：单文件 HTML 部署 | 5 分钟 |
| 第 4 章 | 方式 B：本地服务部署 | 20 分钟 |
| 第 5 章 | 方式 C：Docker 容器化部署 | 30 分钟 |
| 第 6 章 | 方式 D：离线 ISO 部署（无网环境） | 45 分钟 |
| 第 7 章 | 5 个本地 AI 工具部署详解 | 30 分钟 |
| 第 8 章 | Edge-Cloud Protocol v1.0 配置 | 15 分钟 |
| 第 9 章 | 19 维质量门验证 | 15 分钟 |
| 第 11 章 | 安全合规配置 | 15 分钟 |
| 第 12 章 | 监控与运维 | 20 分钟 |
| 第 13 章 | 故障排查（FAQ） | 持续更新 |
| 第 14 章 | 升级与回滚 | 10 分钟 |
| 附录 A | 完整命令清单 | - |
| 附录 B | 环境变量参考 | - |

**总阅读时间 ≈ 4 小时** | **完整部署实践 ≈ 1-3 天**

---

## 第 1 章 · 部署前准备

### 1.1 硬件要求

#### 1.1.1 最低配置（教师个人版）

| 组件 | 最低 | 推荐 | 备注 |
|------|------|------|------|
| CPU | Intel i5-10500 | **Intel 酷睿 Ultra 7 155H** | 必需含 NPU |
| NPU | 不强制 | **Intel AI Boost 11 TOPS** | V7 NPU 调度核心 |
| GPU | Intel UHD 630 | Intel Arc / Iris Xe | iGPU 加速 VLM |
| 内存 | 8 GB | **16 GB LPDDR5** | VLM 需 ≥ 16GB |
| 硬盘 | 256 GB SSD | **512 GB NVMe SSD** | 模型 + 知识库 |
| 网络 | 10 Mbps | 100 Mbps | 云端调用需要 |

#### 1.1.2 推荐配置（学校机房 / 教研组版）

| 组件 | 配置 | 数量 | 备注 |
|------|------|------|------|
| 服务器 | Intel 酷睿 Ultra 9 + 32GB + 1TB NVMe | 1 台 | 主服务器 |
| 工作站 | Intel 酷睿 Ultra 7 + 16GB | 10-50 台 | 教师终端 |
| 交换机 | 千兆 | 1 台 | 内网互联 |
| NAS | 10 TB RAID5 | 1 台 | 共享知识库 |

#### 1.1.3 商用级配置（区域教育云）

- 8 节点集群（每节点 32 TOPS NPU = 256 TOPS 总算力）
- 100 Gbps 内网
- 10 TB 共享存储
- 99.9% SLA

### 1.2 软件要求

#### 1.2.1 操作系统

| OS | 版本 | 推荐度 | 备注 |
|----|------|--------|------|
| Windows | 11 23H2+ | ⭐⭐⭐⭐⭐ | V7 默认开发环境 |
| macOS | 14+ (M2/M3) | ⭐⭐⭐⭐ | Apple Silicon NPU |
| Ubuntu | 22.04 LTS+ | ⭐⭐⭐⭐⭐ | Linux 服务器首选 |
| Deepin | V23+ | ⭐⭐⭐⭐ | 国产化替代 |
| 统信 UOS | V20+ | ⭐⭐⭐⭐ | 信创场景 |

#### 1.2.2 运行时环境

| 软件 | 版本 | 用途 |
|------|------|------|
| Python | 3.9-3.11 | 后端服务 |
| Node.js | 18+ | 前端构建 |
| OpenVINO | 2024.3+ | NPU/iGPU 推理 |
| PaddlePaddle | 2.5+ | OCR 引擎 |
| FFmpeg | 6.0+ | 音视频处理 |
| Qdrant/ChromaDB | latest | RAG 向量库 |
| Docker | 24+ | 容器化（可选） |
| Nginx | 1.24+ | 反向代理（可选） |

#### 1.2.3 浏览器

- **Chrome 120+**（推荐）
- **Edge 120+**
- **Firefox 120+**
- 不支持 IE

### 1.3 网络要求

#### 1.3.1 端口规划

| 端口 | 服务 | 协议 | 防火墙策略 |
|------|------|------|----------|
| 80/443 | Web 前端（Nginx） | HTTP/HTTPS | 公开 |
| **8900** | **V7 Gateway（端云路由）** | HTTP | **仅内网** |
| 8901 | OCR 微服务 | HTTP | 仅内网 |
| 8902 | ASR 微服务 | HTTP/WS | 仅内网 |
| 8903 | TTS 微服务 | HTTP/WS | 仅内网 |
| 8904 | RAG 微服务 | HTTP | 仅内网 |
| 8905 | 数据分析服务 | HTTP | 仅内网 |
| 22 | SSH 管理 | SSH | 仅管理员 IP |

#### 1.3.2 出站白名单

V7 仅在以下场景访问外网（云端轻决策）：

| 域名 | 用途 | 流量 |
|------|------|------|
| `api.openai.com` | LLM 创意决策 | < 10KB/请求 |
| `api.anthropic.com` | LLM 创意决策 | < 10KB/请求 |
| `dashscope.aliyuncs.com` | Qwen Cloud | < 10KB/请求 |
| `*.openai.com` | OpenAI Fallback | < 10KB/请求 |

**入站策略：完全禁止**（V7 不需要任何公网入站）。

### 1.4 模型准备

V7 需要下载以下 AI 模型（建议放置 `/opt/ai-literacy/models/`）：

| 模型 | 大小 | 用途 | 端口 | 量化 |
|------|------|------|------|------|
| PaddleOCR v4 | 200 MB | OCR 文字识别 | 8901 | INT8 |
| Whisper-small | 460 MB | ASR 语音识别 | 8902 | INT4 |
| FunASR Paraformer | 220 MB | ASR 中文（备选） | 8902 | INT4 |
| FastSpeech2 + HiFi-GAN | 150 MB | TTS 语音合成 | 8903 | FP16 |
| VITS | 280 MB | TTS 高质量（备选） | 8903 | FP16 |
| BGE-small-zh | 100 MB | RAG 中文向量 | 8904 | INT8 |
| **Qwen2.5-VL-7B-int4** | 5 GB | **VLM 视频/图像理解** | 8906 | INT4 |
| Qwen-1.5B | 2.5 GB | 端侧 LLM（降级用） | 8907 | INT4 |

**总模型大小：≈ 8.9 GB** | 推荐预留：20 GB（含备份）

### 1.5 部署前 7 项检查清单

- [ ] 确认 Intel 酷睿 Ultra 处理器（含 NPU）
- [ ] 安装 OpenVINO 2024.3+ 与 NPU 驱动
- [ ] 下载所有 AI 模型（建议 8.9 GB）
- [ ] 配置防火墙（仅开放 80/443 + 22）
- [ ] 准备 SSL 证书（Let's Encrypt / 自签）
- [ ] 准备云端 API Key（OpenAI/Anthropic/Qwen）
- [ ] 培训运维人员（≥ 2 人）

---

## 第 2 章 · 4 种部署方式对比

### 2.1 对比总览

| 维度 | 方式 A 单文件 | 方式 B 本地服务 | 方式 C Docker | 方式 D 离线 ISO |
|------|--------------|----------------|--------------|----------------|
| **适用规模** | 1-5 教师 | 5-100 教师 | 100-1000 教师 | 保密/无网单位 |
| **部署时间** | 1 分钟 | 20 分钟 | 30 分钟 | 45 分钟 |
| **硬件要求** | 任意 | i5 + 8GB | i7 + 16GB | 服务器级 |
| **AI 工具链** | ❌ 不可用 | ✅ 全部 | ✅ 全部 | ✅ 全部 |
| **NPU 加速** | ❌ | ✅ | ✅ | ✅ |
| **网络依赖** | 仅云端 LLM | 仅云端 LLM | 仅云端 LLM | **完全离线** |
| **适合场景** | 个人试用 | 学校教研组 | 区/校 SaaS | 信创/保密单位 |

### 2.2 选择决策树

```
Q1: 是否有外网？
├─ ❌ 无网 → 方式 D（离线 ISO）
└─ ✅ 有网
   │
   Q2: 用户规模？
   ├─ 1-5 → 方式 A（单文件）
   ├─ 5-100 → 方式 B（本地服务）
   └─ 100+ → 方式 C（Docker）
```

### 2.3 推荐组合

| 场景 | 推荐组合 |
|------|----------|
| 教师个人试用 | A + 云端 LLM |
| 学校教研组 | B + NPU 加速 |
| 区/市教育云 | C + K8s 集群 |
| 保密单位/军工 | D + 国产化 |
| 混合云（公有云+本地） | B + 公网 API |

---

## 第 3 章 · 方式 A：单文件 HTML 部署

### 3.1 适用场景
- 个人教师试用
- 课堂 5 分钟演示
- 无需 AI 工具链（仅前端交互）

### 3.2 部署步骤

#### 步骤 1：下载 V7 单文件
```bash
# 从 SKILL 包中获取
cp ~/.trae-cn/skills/ai-literacy-expert-v7/manifest/single-file.html ~/Desktop/
```

#### 步骤 2：双击打开
```bash
# Windows
start ~\Desktop\single-file.html

# macOS
open ~/Desktop/single-file.html
```

#### 步骤 3：配置云端 API（可选）
打开浏览器 → 右上角"设置" → 填入 OpenAI API Key → 保存

### 3.3 验证清单
- [ ] HTML 正常打开
- [ ] p5.js 课件可正常播放
- [ ] 互动按钮可点击
- [ ] （可选）云端 LLM 调用成功

### 3.4 限制说明
- ❌ 不含本地 AI 工具（OCR/ASR/TTS/RAG）
- ❌ 不含 NPU 调度
- ✅ 仅前端交互 + 云端 LLM（可选）
- ✅ 适合快速验证和演示

---

## 第 4 章 · 方式 B：本地服务部署

### 4.1 适用场景
- 学校教研组（5-100 教师）
- 完整 AI 工具链
- 端云协同全功能

### 4.2 系统架构

```
┌─────────────────────────────────────────────────┐
│  教师浏览器（Chrome/Edge）                         │
│  http://server-ip:80                              │
└─────────────────┬───────────────────────────────┘
                  ↓ HTTPS
┌─────────────────────────────────────────────────┐
│  Nginx（反向代理 + SSL 终止）                       │
│  /api → :8900  ·  / → 静态文件                     │
└─────────────────┬───────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────┐
│  V7 Gateway :8900（端云路由 + 审计）              │
│  ┌──────┬──────┬──────┬──────┬──────┬────────┐  │
│  │ OCR  │ ASR  │ TTS  │ RAG  │ VLM  │Analysis│  │
│  │:8901 │:8902 │:8903 │:8904 │:8906 │  :8905 │  │
│  └──────┴──────┴──────┴──────┴──────┴────────┘  │
│         ↓ OpenVINO Runtime                        │
│  ┌──────┬──────┬──────────────┐                  │
│  │ NPU  │ iGPU │   CPU        │                  │
│  │ 11T  │ 8T   │  通用协调    │                  │
│  └──────┴──────┴──────────────┘                  │
└─────────────────────────────────────────────────┘
                  ↓ 元数据（< 10KB/请求）
            [云端 LLM：OpenAI/Anthropic/Qwen]
```

### 4.3 部署步骤

#### 步骤 1：环境准备

```bash
# 1.1 安装 Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip

# 1.2 创建项目目录
sudo mkdir -p /opt/ai-literacy
cd /opt/ai-literacy

# 1.3 创建 Python 虚拟环境
python3.11 -m venv venv
source venv/bin/activate

# 1.4 升级 pip
pip install --upgrade pip
```

#### 步骤 2：安装 V7 核心依赖

```bash
# 2.1 安装 OpenVINO（核心推理框架）
pip install openvino==2024.3.0 openvino-dev[onnx,pytorch]==2024.3.0

# 2.2 安装 NNCF（量化工具）
pip install nncf==2.10.0

# 2.3 安装 AI 工具包
pip install paddlepaddle==2.5.2 paddleocr==2.7.3          # OCR
pip install openai-whisper funasr==0.8.7                # ASR
pip install TTS==0.22.0                                # TTS
pip install chromadb==0.4.24 sentence-transformers==2.7 # RAG
pip install transformers==4.40 torch==2.3             # VLM
pip install pandas==2.2 plotly==5.20 matplotlib==3.9    # Analysis

# 2.4 安装 Web 框架
pip install fastapi==0.111 uvicorn[standard]==0.30 httpx==0.27
pip install python-multipart pydantic==2.7 websockets==12.0
```

#### 步骤 3：下载 AI 模型

```bash
# 3.1 创建模型目录
sudo mkdir -p /opt/ai-literacy/models
cd /opt/ai-literacy/models

# 3.2 下载 PaddleOCR（v4 INT8，200 MB）
wget https://paddleocr.bj.bcebos.com/PP-OCRv4/chinese/ch_PP-OCRv4_det_infer.tar
wget https://paddleocr.bj.bcebos.com/PP-OCRv4/chinese/ch_PP-OCRv4_rec_infer.tar
wget https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_mobile_v2.0_cls_train.tar
tar -xf ch_PP-OCRv4_det_infer.tar && tar -xf ch_PP-OCRv4_rec_infer.tar && tar -xf ch_ppocr_mobile_v2.0_cls_train.tar
mo --input_model ch_PP-OCRv4_det_infer --model_name paddleocr_v4_det_int8
mo --input_model ch_PP-OCRv4_rec_infer --model_name paddleocr_v4_rec_int8

# 3.3 下载 Whisper-small INT4
pip install openvino-genai==2024.3.0
optimum-cli export openvino --model openai/whisper-small --task automatic-speech-recognition whisper-small-int4

# 3.4 下载 FastSpeech2 + HiFi-GAN（FP16）
git clone https://github.com/espnet/espnet.git
cd espnet && pip install -e .
# 下载预训练 FastSpeech2
wget https://huggingface.co/espnet/kan-bayashi_ljspeech_fastspeech2/resolve/main/model.pkl

# 3.5 下载 BGE-small-zh INT8
optimum-cli export openvino --model BAAI/bge-small-zh --task feature-extraction bge-small-zh-int8

# 3.6 下载 Qwen2.5-VL-7B INT4（关键！）
optimum-cli export openvino --model Qwen/Qwen2.5-VL-7B-Instruct --task image-text-to-text qwen-vl-7b-int4
# 模型大小约 5 GB

# 3.7 下载端侧 LLM（Qwen-1.5B INT4 降级用）
optimum-cli export openvino --model Qwen/Qwen2-1.5B-Instruct --task text-generation qwen-1.5b-int4

# 3.8 验证模型
ls -la /opt/ai-literacy/models/
du -sh /opt/ai-literacy/models/  # 应约 8.9 GB
```

#### 步骤 4：部署 V7 Gateway + 5 微服务

```bash
# 4.1 复制 V7 Skill 到部署目录
sudo cp -r ~/.trae-cn/skills/ai-literacy-expert-v7 /opt/ai-literacy/skill
cd /opt/ai-literacy/skill

# 4.2 创建服务配置
cat > /opt/ai-literacy/config/services.yaml << 'EOF'
gateway:
  host: 0.0.0.0
  port: 8900
  enable_audit: true
  zup_storage: /var/log/ai-literacy/zup/
  zup_retention_days: 30

ocr:
  host: 0.0.0.0
  port: 8901
  model: paddleocr_v4_int8
  device: NPU
  confidence_threshold: 0.85

asr:
  host: 0.0.0.0
  port: 8902
  model: whisper-small-int4
  device: NPU
  language: auto
  enable_evaluate: true

tts:
  host: 0.0.0.0
  port: 8903
  model: fastspeech2
  device: NPU
  default_voice: xiaoxiao
  voices:
    - xiaoxiao
    - xiaoyun
    - xiaochen
    - xiaomo

rag:
  host: 0.0.0.0
  port: 8904
  embedding_model: bge-small-zh-int8
  vector_db: chromadb
  storage_path: /var/lib/ai-literacy/chromadb/
  enable_rerank: true

analysis:
  host: 0.0.0.0
  port: 8905
  enable_plotly: true
  cache_results: true

vlm:
  host: 0.0.0.0
  port: 8906
  model: qwen-vl-7b-int4
  device: GPU
  max_new_tokens: 512

local_llm:
  host: 0.0.0.0
  port: 8907
  model: qwen-1.5b-int4
  device: CPU
  enabled: true  # 降级用
EOF

# 4.3 启动所有服务（使用 systemd）
cat > /etc/systemd/system/ai-literacy-gateway.service << 'EOF'
[Unit]
Description=V7 AI Literacy Gateway
After=network.target

[Service]
Type=simple
User=ai-literacy
WorkingDirectory=/opt/ai-literacy/skill
Environment="PATH=/opt/ai-literacy/venv/bin"
ExecStart=/opt/ai-literacy/venv/bin/python -m ai_literacy_gateway --config /opt/ai-literacy/config/services.yaml
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 类似地创建 5 个微服务 + VLM + 本地 LLM 的 systemd unit...
# ocr.service / asr.service / tts.service / rag.service / analysis.service / vlm.service / local-llm.service

# 4.4 创建用户和目录
sudo useradd -r -s /bin/false ai-literacy
sudo chown -R ai-literacy:ai-literacy /opt/ai-literacy /var/lib/ai-literacy /var/log/ai-literacy

# 4.5 启动服务
sudo systemctl daemon-reload
sudo systemctl enable --now ai-literacy-gateway
sudo systemctl enable --now ai-literacy-ocr
sudo systemctl enable --now ai-literacy-asr
sudo systemctl enable --now ai-literacy-tts
sudo systemctl enable --now ai-literacy-rag
sudo systemctl enable --now ai-literacy-analysis
sudo systemctl enable --now ai-literacy-vlm
sudo systemctl enable --now ai-literacy-local-llm

# 4.6 检查状态
sudo systemctl status ai-literacy-gateway
sudo systemctl status ai-literacy-ocr
curl http://localhost:8900/health
curl http://localhost:8901/health
curl http://localhost:8902/health
curl http://localhost:8903/health
curl http://localhost:8904/health
curl http://localhost:8905/health
curl http://localhost:8906/health
```

#### 步骤 5：配置 Nginx 反向代理

```bash
# 5.1 安装 Nginx
sudo apt install nginx

# 5.2 配置 V7 站点
cat > /etc/nginx/sites-available/ai-literacy << 'EOF'
server {
    listen 80;
    server_name ai-literacy.your-school.edu;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name ai-literacy.your-school.edu;

    ssl_certificate /etc/ssl/certs/ai-literacy.crt;
    ssl_certificate_key /etc/ssl/private/ai-literacy.key;
    ssl_protocols TLSv1.2 TLSv1.3;

    # 前端静态文件
    root /opt/ai-literacy/skill/frontend/dist;
    index index.html;

    # API 反向代理
    location /api/ {
        proxy_pass http://localhost:8900/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 300s;
    }

    # WebSocket 支持
    location /ws/ {
        proxy_pass http://localhost:8900/ws/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # 安全头
    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options "nosniff";
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
    add_header Content-Security-Policy "default-src 'self' 'unsafe-inline' 'unsafe-eval'; img-src 'self' data: blob:; media-src 'self' blob:";
}

# 限流（防止滥用）
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=30r/m;

server {
    listen 80 default_server;
    server_name _;

    location /api/ {
        limit_req zone=api_limit burst=20 nodelay;
        proxy_pass http://localhost:8900/;
    }
}
EOF

# 5.3 启用站点
sudo ln -s /etc/nginx/sites-available/ai-literacy /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 步骤 6：配置 SSL 证书

```bash
# 6.1 Let's Encrypt（推荐）
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d ai-literacy.your-school.edu

# 6.2 自动续期
sudo certbot renew --dry-run

# 6.3 自签证书（测试环境）
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/ai-literacy.key \
  -out /etc/ssl/certs/ai-literacy.crt \
  -subj "/CN=ai-literacy.local"
```

#### 步骤 7：初始化 RAG 知识库

```bash
# 7.1 创建知识库
mkdir -p /var/lib/ai-literacy/chromadb/

# 7.2 导入 V7 课程模块文档
python -m ai_literacy.rag.import_docs \
  --source /opt/ai-literacy/skill/references/ \
  --collection teaching_kb

# 7.3 导入课程标准
python -m ai_literacy.rag.import_docs \
  --source /path/to/curriculum_standards/ \
  --collection curriculum_standards

# 7.4 验证
python -m ai_literacy.rag.query \
  --query "Prompt 五要素" \
  --top-k 3
```

#### 步骤 8：配置云端 LLM API Key

```bash
# 创建环境变量文件
cat > /opt/ai-literacy/config/secrets.env << 'EOF'
# 云端 LLM（端云协同的"云端轻决策"）
OPENAI_API_KEY=REDACTED-SECRET
ANTHROPIC_API_KEY=REDACTED-SECRET
QWEN_API_KEY=sk-xxxxxxxxxxxxxxxx

# 启用 Fallback
ENABLE_CLOUD_FALLBACK=true
DEFAULT_LLM_PROVIDER=openai  # openai | anthropic | qwen
EOF

# 加密
sudo chmod 600 /opt/ai-literacy/config/secrets.env
```

### 4.4 验证清单
- [ ] 所有 7 个 systemd 服务运行中
- [ ] 7 个微服务 health 端点返回 200
- [ ] Nginx 反向代理正常
- [ ] SSL 证书有效
- [ ] 浏览器可访问 https://ai-literacy.your-school.edu
- [ ] 知识库已初始化
- [ ] 云端 API Key 已配置

---

## 第 5 章 · 方式 C：Docker 容器化部署

### 5.1 适用场景
- 大规模部署（100+ 用户）
- 集群化 / Kubernetes
- DevOps 集成

### 5.2 docker-compose.yml

```yaml
version: '3.8'

services:
  # V7 Gateway（主入口）
  gateway:
    image: ai-literacy/gateway:v7.0.0
    container_name: v7-gateway
    restart: always
    ports:
      - "8900:8900"
    environment:
      - GATEWAY_PORT=8900
      - ENABLE_AUDIT=true
      - ZUP_STORAGE=/var/log/zup
    volumes:
      - v7-zup:/var/log/zup
      - ./config/gateway.yaml:/app/config/services.yaml
    depends_on:
      - ocr
      - asr
      - tts
      - rag
      - analysis
      - vlm
    networks:
      - ai-net

  # OCR 微服务
  ocr:
    image: ai-literacy/ocr:v7.0.0
    container_name: v7-ocr
    restart: always
    ports:
      - "8901:8901"
    environment:
      - OCR_MODEL=paddleocr_v4_int8
      - OPENVINO_DEVICE=NPU
    volumes:
      - v7-models:/opt/models
    networks:
      - ai-net

  # ASR 微服务
  asr:
    image: ai-literacy/asr:v7.0.0
    container_name: v7-asr
    restart: always
    ports:
      - "8902:8902"
    environment:
      - ASR_MODEL=whisper-small-int4
      - OPENVINO_DEVICE=NPU
      - ENABLE_EVALUATE=true
    volumes:
      - v7-models:/opt/models
    networks:
      - ai-net

  # TTS 微服务
  tts:
    image: ai-literacy/tts:v7.0.0
    container_name: v7-tts
    restart: always
    ports:
      - "8903:8903"
    environment:
      - TTS_MODEL=fastspeech2
      - OPENVINO_DEVICE=NPU
      - DEFAULT_VOICE=xiaoxiao
    volumes:
      - v7-models:/opt/models
    networks:
      - ai-net

  # RAG 微服务
  rag:
    image: ai-literacy/rag:v7.0.0
    container_name: v7-rag
    restart: always
    ports:
      - "8904:8904"
    environment:
      - EMBEDDING_MODEL=bge-small-zh-int8
      - VECTOR_DB=chromadb
    volumes:
      - v7-rag-data:/var/lib/chromadb
      - v7-models:/opt/models
    networks:
      - ai-net

  # VLM 视频理解（V7 关键）
  vlm:
    image: ai-literacy/vlm:v7.0.0
    container_name: v7-vlm
    restart: always
    ports:
      - "8906:8906"
    environment:
      - VLM_MODEL=qwen-vl-7b-int4
      - OPENVINO_DEVICE=GPU
    volumes:
      - v7-models:/opt/models
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    networks:
      - ai-net

  # 数据分析
  analysis:
    image: ai-literacy/analysis:v7.0.0
    container_name: v7-analysis
    restart: always
    ports:
      - "8905:8905"
    environment:
      - ENABLE_PLOTLY=true
    networks:
      - ai-net

  # Nginx 前端
  frontend:
    image: nginx:1.25-alpine
    container_name: v7-frontend
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./frontend/dist:/usr/share/nginx/html:ro
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - ./ssl:/etc/ssl:ro
    depends_on:
      - gateway
    networks:
      - ai-net

  # 监控（可选）
  prometheus:
    image: prom/prometheus:latest
    container_name: v7-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
    networks:
      - ai-net

  grafana:
    image: grafana/grafana:latest
    container_name: v7-grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=v7admin
    depends_on:
      - prometheus
    networks:
      - ai-net

volumes:
  v7-models:
    driver: local
  v7-rag-data:
    driver: local
  v7-zup:
    driver: local

networks:
  ai-net:
    driver: bridge
```

### 5.3 部署命令

```bash
# 1. 创建项目目录
mkdir -p /opt/v7 && cd /opt/v7

# 2. 复制配置文件
cp ~/.trae-cn/skills/ai-literacy-expert-v7/deploy/docker-compose.yml .
cp ~/.trae-cn/skills/ai-literacy-expert-v7/deploy/.env .

# 3. 配置环境变量
cat > .env << 'EOF'
# 版本
V7_VERSION=7.0.0
# API Keys
OPENAI_API_KEY=sk-xxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxx
# 镜像仓库
REGISTRY=your-registry.com/ai-literacy
EOF

# 4. 拉取镜像
docker-compose pull

# 5. 启动
docker-compose up -d

# 6. 查看状态
docker-compose ps

# 7. 查看日志
docker-compose logs -f gateway

# 8. 健康检查
curl http://localhost:8900/health
curl http://localhost:8901/health
curl http://localhost:8902/health
curl http://localhost:8903/health
curl http://localhost:8904/health
curl http://localhost:8905/health
curl http://localhost:8906/health
```

### 5.4 Kubernetes 部署（高级）

```yaml
# v7-gateway-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: v7-gateway
spec:
  replicas: 3
  selector:
    matchLabels:
      app: v7-gateway
  template:
    metadata:
      labels:
        app: v7-gateway
    spec:
      containers:
      - name: gateway
        image: ai-literacy/gateway:v7.0.0
        ports:
        - containerPort: 8900
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: v7-secrets
              key: openai-key
---
apiVersion: v1
kind: Service
metadata:
  name: v7-gateway
spec:
  selector:
    app: v7-gateway
  ports:
  - port: 8900
    targetPort: 8900
  type: LoadBalancer
```

```bash
kubectl apply -f v7-gateway-deployment.yaml
kubectl get pods -l app=v7-gateway
kubectl logs -f deployment/v7-gateway
```

### 5.5 验证清单
- [ ] docker-compose ps 显示 7+ 服务 healthy
- [ ] 所有微服务 health 端点返回 200
- [ ] Nginx 80/443 可访问
- [ ] Prometheus 9090 收集到指标
- [ ] Grafana 3000 可视化正常
- [ ] K8s pods 全部 Ready（如使用 K8s）

---

## 第 6 章 · 方式 D：离线 ISO 部署（无网环境）

### 6.1 适用场景
- 保密单位 / 军工 / 政府内网
- 校园网未覆盖
- 网络管控严格

### 6.2 ISO 镜像构建

#### 步骤 1：准备构建环境（需要联网）

```bash
# 1.1 安装 ISO 构建工具
sudo apt install xorriso genisoimage isolinux syslinux-utils

# 1.2 创建构建目录
mkdir -p /tmp/v7-iso/{boot,casper,isolinux}
cd /tmp/v7-iso

# 1.3 下载 V7 完整包（含所有模型）
wget https://your-server.com/v7-7.0.0-full.tar.gz
tar -xzf v7-7.0.0-full.tar.gz

# 1.4 准备 Ubuntu Live 基础
# 下载 ubuntu-22.04.3-live-server-amd64.iso
# 提取文件系统
sudo mount -o loop ubuntu-22.04.3-live-server-amd64.iso /mnt
sudo cp -r /mnt/* casper/
sudo umount /mnt

# 1.5 集成 V7 Skill
sudo cp -r v7-7.0.0-full casper/opt/ai-literacy/

# 1.6 预装所有 Python 依赖（whl 离线包）
mkdir -p casper/opt/pip-packages
pip download -r v7-7.0.0-full/requirements.txt -d casper/opt/pip-packages/

# 1.7 制作自动安装脚本
cat > casper/opt/ai-literacy/install.sh << 'EOF'
#!/bin/bash
# V7 离线自动安装脚本
set -e
echo "=== V7 离线自动安装 ==="

# 安装 Python 依赖
pip install --no-index --find-links=/opt/pip-packages/ -r /opt/ai-literacy/requirements.txt

# 复制模型
mkdir -p /opt/ai-literacy/models/
cp -r /opt/ai-literacy/models-bundled/* /opt/ai-literacy/models/

# 启动服务
systemctl enable --now ai-literacy-gateway
systemctl enable --now ai-literacy-ocr
systemctl enable --now ai-literacy-asr
systemctl enable --now ai-literacy-tts
systemctl enable --now ai-literacy-rag
systemctl enable --now ai-literacy-analysis
systemctl enable --now ai-literacy-vlm

echo "✅ V7 离线安装完成"
echo "访问 http://localhost 即可使用"
EOF
chmod +x casper/opt/ai-literacy/install.sh
```

#### 步骤 2：生成 ISO

```bash
# 2.1 配置启动菜单
cat > isolinux/grub.cfg << 'EOF'
set timeout=10
set default=0

menuentry "V7 ai-literacy-expert v7.0.0 离线安装" {
    linux /casper/vmlinuz boot=casper quiet splash autoinstall ds=nocloud;s=/cdrom/preseed/
    initrd /casper/initrd
}
menuentry "V7 试用模式（不安装）" {
    linux /casper/vmlinuz boot=casper quiet splash --
    initrd /casper/initrd
}
EOF

# 2.2 预安装配置
cat > casper/preseed/user-data << 'EOF'
#cloud-config
autoinstall:
  version: 1
  locale: zh_CN.UTF-8
  keyboard:
    layout: cn
  identity:
    hostname: ai-literacy
    username: ai-literacy
    password: "$6$rounds=4096$..."
  packages:
    - python3.11
    - python3-pip
    - nginx
    - nodejs
    - npm
  late-commands:
    - ["bash", "/opt/ai-literacy/install.sh"]
EOF

# 2.3 生成 ISO
grub-mkrescue -o v7-ai-literacy-7.0.0-offline.iso /tmp/v7-iso/

# 2.4 验证
ls -lh v7-ai-literacy-7.0.0-offline.iso
# 应约 12-15 GB（含所有模型）
```

### 6.3 ISO 安装（目标机器）

```bash
# 3.1 制作 U 盘启动盘
sudo dd if=v7-ai-literacy-7.0.0-offline.iso of=/dev/sdb bs=4M status=progress

# 3.2 启动目标机器 → 选择"V7 安装"
# 3.3 自动安装（约 15 分钟）
# 3.4 安装完成 → 自动启动所有服务
# 3.5 浏览器访问 http://本机IP
```

### 6.4 验证清单
- [ ] ISO 镜像 ≥ 10 GB
- [ ] 目标机器可从 U 盘启动
- [ ] 自动安装 15 分钟内完成
- [ ] 7 个服务全部启动（systemctl list-units --type=service | grep ai-literacy）
- [ ] 完全离线可工作（拔网线测试）

---

## 第 7 章 · 5 个本地 AI 工具部署详解

### 7.1 OCR 工具（端口 8901）

#### 7.1.1 PaddleOCR v4 部署

```bash
# 验证 NPU 可用
python -c "from openvino.runtime import Core; print(Core().available_devices)"
# 应输出: ['CPU', 'GPU', 'NPU']

# 测试 OCR
python -c "
from paddleocr import PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='ch', use_gpu=False, enable_mkldnn=True)
result = ocr.ocr('/path/to/test.png', cls=True)
for line in result[0]:
    print(line[1])
"

# NPU 量化模型
mo --input_model paddleocr_v4_det_onnx \
   --model_name paddleocr_v4_det_int8 \
   --compress_to_fp16=False
```

#### 7.1.2 OCR API 调用示例

```bash
curl -X POST http://localhost:8901/recognize \
  -H "Content-Type: application/json" \
  -d '{
    "image": "base64_encoded_image_data",
    "output_format": "structured",
    "detect_table": true,
    "detect_formula": true
  }'
```

### 7.2 ASR 工具（端口 8902）

```bash
# 测试 ASR
python -c "
from faster_whisper import WhisperModel
model = WhisperModel('whisper-small-int4', device='cpu', compute_type='int4')
segments, info = model.transcribe('test.wav', beam_size=5)
for segment in segments:
    print(f'[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}')
"

# ASR 评测
curl -X POST http://localhost:8902/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "reference": "Prompt 五要素分别是什么？",
    "hypothesis": "Prompt五要素分别是什么呢"
  }'
```

### 7.3 TTS 工具（端口 8903）

```bash
# 测试 TTS
python -c "
from TTS.api import Synthesizer
synthesizer = Synthesizer('tts_models/zh-CN/baker/tacotron2-DDC-GST/model.pkl')
synthesizer.tts('你好，欢迎使用 V7')
"

# 4 音色列表
curl http://localhost:8903/voices
# ["xiaoxiao", "xiaoyun", "xiaochen", "xiaomo"]
```

### 7.4 RAG 工具（端口 8904）

```bash
# 初始化 ChromaDB
python -c "
import chromadb
client = chromadb.PersistentClient(path='/var/lib/ai-literacy/chromadb')
collection = client.create_collection('teaching_kb')

# 导入 V7 课程模块
import os
for f in os.listdir('/opt/ai-literacy/skill/references/module-*.md'):
    with open(f) as fp:
        collection.add(documents=[fp.read()], ids=[f])
"

# 查询
curl -X POST http://localhost:8904/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Prompt 五要素", "top_k": 3, "collection": "teaching_kb"}'
```

### 7.5 Analysis 工具（端口 8905）

```bash
# 启动 Plotly
python -m ai_literacy.analysis.server --port 8905

# 成绩分析
curl -X POST http://localhost:8905/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "data": [...],
    "analysis_type": "score_stats",
    "options": {"chart_type": "bar"}
  }'
```

### 7.6 VLM 工具（端口 8906 · V7 关键）

```bash
# Qwen2.5-VL-7B INT4 部署
python -c "
from openvino_genai import VLMPipeline
pipe = VLMPipeline('qwen-vl-7b-int4', 'GPU')
"

# 视频抽帧分析
curl -X POST http://localhost:8906/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "videos": ["base64_frame_1", "base64_frame_2", ...],
    "prompt": "分析这个视频片段的教学内容"
  }'
```

---

## 第 8 章 · Edge-Cloud Protocol v1.0 配置

### 8.1 协议基础

V7 端云交互使用标准化 Edge-Cloud Protocol v1.0，所有请求必须遵守 6 段结构 + 4 大核心约束。

### 8.2 协议配置

```yaml
# /opt/ai-literacy/config/protocol.yaml
edge_cloud_protocol:
  version: "1.0"
  max_abstract_data_bytes: 10240        # 约束 1
  require_pii_false: true               # 约束 2
  local_retention_days: 7               # 约束 3
  decision_types:                       # 4 类决策
    - creative
    - analytical
    - educational
    - strategic
  degradation:
    enabled: true
    levels: 5                           # L1-L5
  error_codes:
    E001_to_E202: 9_codes
```

### 8.3 协议调试

```bash
# 启动协议调试器
python -m ai_literacy.protocol_debugger

# 测试合规请求
curl -X POST http://localhost:8900/api/v1/edge-cloud/exchange \
  -H "Content-Type: application/json" \
  -d '{
    "protocol_version": "1.0",
    "request_id": "req-001",
    "timestamp": "2026-08-15T10:00:00Z",
    "source": "edge-ai-pc",
    "intent": "教学策略推荐",
    "abstract": {
      "task_type": "pedagogy_recommendation",
      "context": "高一(3)班 · 期中复习",
      "abstract_data": {"avg_score": 78.5},
      "pii_detected": false,
      "data_classification": "anonymous"
    },
    "request": {
      "decision_type": "educational",
      "max_tokens": 500,
      "max_cost_usd": 0.001
    },
    "callback": {
      "edge_execution": true,
      "save_to_local": true
    }
  }'
```

### 8.4 5 级降级策略

| Level | 触发条件 | 行为 |
|-------|----------|------|
| L1 | 云端 OK | 端云协同 · max_tokens 500 |
| L2 | 云端慢 | max_tokens 250 |
| L3 | 云端不可用 | 端侧 LLM（Qwen-1.5B）|
| L4 | 端侧 LLM 不可用 | 规则+模板 |
| L5 | 全部不可用 | 完全本地 + 提示用户 |

---

## 第 9 章 · 19 维质量门验证

### 9.1 V6 继承 15 维

| # | 维度 | 验证方法 | 自动化脚本 |
|---|------|----------|----------|
| 1 | HTML 结构 | grep DOCTYPE | 人工 / `grep '<!DOCTYPE' *.html` |
| 2 | p5.js 2.x | grep "p5@2" | 人工 / `grep 'p5@2' *.html` |
| 3 | 单文件 | check size | 人工 / `du -sh *.html` |
| 4 | 中文内容 | check encoding | 人工 / `file -i *.html` |
| 5 | 教学准确 | manual review | - |
| 6 | 交互完整 | e2e test | 人工 / 浏览器测试 |
| 7 | 响应式 | visual test | 人工 / 浏览器 DevTools |
| 8 | 无障碍 | WAVE tool | 外部工具 `flake8` |
| 9 | 代码质量 | linter | `flake8` |
| 10 | 离线支持 | network test | 人工 / 断网测试 |
| 11 | 安全合规 | OWASP ZAP | 外部工具 OWASP ZAP |
| 12 | 本地 AI 集成 | integration test | `scripts/edge_cloud_dispatch.py` |
| 13 | 跨平台兼容 | 3 平台测试 | 人工 / `run.ps1` + `run.sh` |
| 14 | Pipeline 完整 | e2e pipeline | `scripts/bootstrap.py` |
| 15 | 商用交付 | checklist | 人工 / `references/commercial-production-standards.md` |

### 9.2 V7 新增 4 维

| # | 维度 | 验证方法 |
|---|------|----------|
| 16 | 端云协同分工验证 | 检查每能力明确标注 |
| 17 | 零上传隐私计算 | grep "pii_detected": false |
| 18 | NPU 智能调度 | `openvino.runtime.Core().available_devices` |
| 19 | 端云成本监控 | `scripts/cost_monitor.py` |

### 9.3 一键验证

```bash
# 运行 33 项单元测试
cd <SKILL_DIR>
python -m unittest discover -s tests -v

# 输出示例：
# test_redact_phone_chinese_context (test_all.TestPIIRedaction)
# ok
# test_redact_id_card (test_all.TestPIIRedaction)
# ok
# ...
# Ran 33 tests in 0.062s
# OK
```

---

## 第 11 章 · 安全合规配置

### 11.1 4 级 PII 自动脱敏

V7 在端侧自动实现 4 级 PII 脱敏，详见 `references/zero-upload-privacy.md`：

- **L1 标识符**：姓名/身份证/手机/邮箱/学号
- **L2 关系**：住址/学校/班级/家长
- **L3 行为**：时间戳/答题路径/行为模式
- **L4 内容**：作文/发言/心理评估

### 11.2 数据生命周期

| 数据类型 | 保留位置 | 保留时长 |
|----------|----------|----------|
| 原始数据 | 端侧 | **7 天**（自动加密删除）|
| 抽象元数据 | 端侧 + 云端 | 30 天 |
| 教学决策 | 端侧 | 永久 |
| 审计日志（ZUP）| 端侧 `/var/log/ai-literacy/zup/` | 永久 |

### 11.3 3 大法规合规

#### 11.3.1 GDPR（欧盟）

- [x] 数据最小化（原始数据 0 上传）
- [x] 目的限制（仅教学用途）
- [x] 存储限制（7 天自动清理）
- [x] 完整性与保密性（HTTPS + 加密）
- [x] 问责制（ZUP 审计）

#### 11.3.2 中国《个人信息保护法》

- [x] 知情同意（用户首次访问需同意）
- [x] 最小必要（仅元数据上传）
- [x] 公开透明（V7 协议开源）
- [x] 数据本地化（端侧优先）
- [x] 安全保障（NPU 隔离 + 端云协议）

#### 11.3.3 COPPA（美国儿童在线隐私保护法）

- [x] 13 岁以下需监护人同意
- [x] 不收集超出必要数据
- [x] 家长可查看/删除数据
- [x] 不用于商业广告

### 11.4 SSL/TLS 配置

```bash
# 强制 HTTPS（Let's Encrypt）
sudo certbot --nginx -d ai-literacy.your-school.edu

# 自签证书（测试环境）
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/ai-literacy.key \
  -out /etc/ssl/certs/ai-literacy.crt
```

### 11.5 防火墙规则

```bash
# 启用 UFW
sudo ufw enable

# 允许 SSH（限制 IP）
sudo ufw allow from 192.168.1.0/24 to any port 22

# 允许 HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 内网 8900-8906 端口（仅内网）
sudo ufw allow from 192.168.1.0/24 to any port 8900:8906 proto tcp

# 默认拒绝入站
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

---

## 第 12 章 · 监控与运维

### 12.1 Prometheus + Grafana 监控

V7 内置 Prometheus 指标端点 `/metrics`：

```yaml
# 关键指标
v7_ocr_requests_total{status="success"} 1234
v7_ocr_latency_seconds{quantile="0.5"} 0.168
v7_ocr_latency_seconds{quantile="0.95"} 0.250

v7_asr_requests_total{status="success"} 856
v7_asr_evaluate_score 92.3

v7_tts_requests_total 234
v7_rag_query_latency_seconds 0.078
v7_analysis_charts_generated 156

v7_edge_cloud_cost_usd_total 0.42
v7_edge_cloud_cache_hit_ratio 0.42
v7_edge_cloud_degradation_level 1

v7_npu_utilization{device="NPU"} 0.65
v7_npu_utilization{device="GPU"} 0.32
v7_npu_utilization{device="CPU"} 0.45

v7_zup_total{pii_detected="false"} 5234
v7_zup_violations_total 0
```

### 12.2 告警规则

```yaml
# /etc/prometheus/rules/v7-alerts.yml
groups:
- name: v7_alerts
  rules:
  - alert: V7ServiceDown
    expr: up{job="v7"} == 0
    for: 2m
    severity: critical
    annotations:
      summary: "V7 服务 {{ $labels.instance }} 宕机"

  - alert: V7ZUPViolation
    expr: v7_zup_violations_total > 0
    severity: high
    annotations:
      summary: "V7 检测到 PII 上传违规"

  - alert: V7EdgeCloudCostHigh
    expr: v7_edge_cloud_cost_usd_total > 20
    for: 1h
    severity: warning
    annotations:
      summary: "V7 云端成本超 $20/月"

  - alert: V7NPUOverload
    expr: v7_npu_utilization{device="NPU"} > 0.9
    for: 5m
    severity: warning
```

### 12.3 日志管理

```bash
# 日志轮转配置
cat > /etc/logrotate.d/ai-literacy << 'EOF'
/var/log/ai-literacy/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 ai-literacy ai-literacy
    sharedscripts
    postrotate
        systemctl reload ai-literacy-gateway
    endscript
}
EOF
```

### 12.4 备份策略

```bash
# 每日自动备份
cat > /opt/ai-literacy/scripts/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR=/var/backups/ai-literacy
DATE=$(date +%Y%m%d)

# 备份 RAG 知识库
tar -czf $BACKUP_DIR/chromadb-$DATE.tar.gz /var/lib/ai-literacy/chromadb/

# 备份 ZUP 审计日志
tar -czf $BACKUP_DIR/zup-$DATE.tar.gz /var/log/ai-literacy/zup/

# 备份配置
cp -r /opt/ai-literacy/config $BACKUP_DIR/config-$DATE/

# 清理 30 天前的备份
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

echo "✅ V7 备份完成: $BACKUP_DIR"
EOF
chmod +x /opt/ai-literacy/scripts/backup.sh

# 加入 crontab
echo "0 2 * * * /opt/ai-literacy/scripts/backup.sh" | sudo crontab -
```

---

## 第 13 章 · 故障排查（FAQ）

### 13.1 服务启动问题

**Q1: `systemctl start ai-literacy-gateway` 失败？**

```bash
# 1. 查看日志
sudo journalctl -u ai-literacy-gateway -n 50

# 2. 常见原因：
#    - 端口被占用: sudo lsof -i :8900
#    - Python 虚拟环境路径错误
#    - 依赖包缺失: pip install -r requirements.txt

# 3. 重新部署
sudo systemctl stop ai-literacy-gateway
source /opt/ai-literacy/venv/bin/activate
cd /opt/ai-literacy/skill
python -m ai_literacy_gateway --config /opt/ai-literacy/config/services.yaml
```

### 13.2 NPU 不可用

**Q2: 报错 "NPU device not found"？**

```bash
# 1. 检查 NPU 驱动
lsmod | grep intel_vpu
dmesg | grep -i npu

# 2. 安装 NPU 驱动（Ubuntu）
sudo apt install intel-vpu-firmware
sudo modprobe intel_vpu

# 3. 验证 OpenVINO 检测
python -c "from openvino.runtime import Core; print(Core().available_devices)"
# 应包含 'NPU'

# 4. 降级到 CPU（应急）
export OPENVINO_DEVICE=CPU
```

### 13.3 OCR 准确率低

**Q3: OCR 识别准确率 < 90%？**

- 检查图片质量（≥ 300 DPI）
- 启用方向分类：`use_angle_cls=True`
- 增加置信度阈值：`confidence_threshold=0.7`
- 训练自定义模型（特定字体）

### 13.4 云端调用失败

**Q4: 云端 LLM 调用失败？**

```bash
# 1. 检查网络
ping api.openai.com
curl -I https://api.openai.com

# 2. 检查 API Key
echo $OPENAI_API_KEY
curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models

# 3. 触发降级（手动）
python -c "
from ai_literacy.edge_cloud import EdgeCloudClient
client = EdgeCloudClient()
client.set_degradation_level(3)  # L3 仅端侧 LLM
"
```

### 13.5 性能问题

**Q5: 端云交互延迟高（> 3s）？**

- 检查 NPU 利用率（过高时降级）
- 启用缓存（命中率应 > 40%）
- 启用压缩（abstract_data < 5KB）
- 升级到 L2 降级

---

## 第 14 章 · 升级与回滚

### 14.1 升级 V7.x → V7.y

```bash
# 1. 备份当前版本
sudo /opt/ai-literacy/scripts/backup.sh
cp -r /opt/ai-literacy /var/backups/v7-x.y.z

# 2. 停止服务
sudo systemctl stop ai-literacy-*

# 3. 下载新版本
cd /opt/ai-literacy
wget https://your-server.com/v7-y.z.tar.gz
tar -xzf v7-y.z.tar.gz --strip-components=1

# 4. 升级依赖
source venv/bin/activate
pip install --upgrade -r requirements.txt

# 5. 启动新版本
sudo systemctl start ai-literacy-*
sudo systemctl status ai-literacy-gateway

# 6. 验证
curl http://localhost:8900/health
python -m ai_literacy.quality_gate.run_all
```

### 14.2 回滚 V7.y → V7.x

```bash
# 1. 停止当前版本
sudo systemctl stop ai-literacy-*

# 2. 恢复备份
sudo rm -rf /opt/ai-literacy
sudo cp -r /var/backups/v7-x.y.z /opt/ai-literacy
sudo chown -R ai-literacy:ai-literacy /opt/ai-literacy

# 3. 启动旧版本
sudo systemctl start ai-literacy-*
```

### 14.3 升级 V6 → V7（重要）

V6 升级到 V7 涉及 references 目录结构调整：

```bash
# 1. 备份 V6
sudo systemctl stop ai-literacy-v6-*
sudo cp -r /opt/ai-literacy-v6 /var/backups/v6-backup

# 2. 安装 V7（按方式 B 步骤）

# 3. 迁移数据
# V6 知识库 → V7
cp /var/lib/ai-literacy-v6/chromadb/* /var/lib/ai-literacy/chromadb/

# V6 配置 → V7（部分兼容）
# V6 配置文件需要适配 V7 的 services.yaml

# 4. 验证
python -m ai_literacy.quality_gate.run_all
```

---

## 附录 A · 完整命令清单（速查）

### A.1 服务管理

```bash
# 查看所有 V7 服务状态
sudo systemctl status ai-literacy-*

# 重启所有服务
sudo systemctl restart ai-literacy-*

# 查看 Gateway 日志
sudo journalctl -u ai-literacy-gateway -f

# 健康检查
curl http://localhost:8900/health
```

### A.2 模型管理

```bash
# 查看已下载模型
ls -lh /opt/ai-literacy/models/

# 重新下载模型
bash /opt/ai-literacy/scripts/download_models.sh

# 验证模型完整性
python -c "
from openvino.runtime import Core
core = Core()
print('Available devices:', core.available_devices)
"
```

### A.3 知识库管理

```bash
# 导入文档到 RAG
python -m ai_literacy.rag.import_docs \
  --source /path/to/docs/ \
  --collection teaching_kb

# 查询 RAG
curl -X POST http://localhost:8904/query \
  -d '{"query": "Prompt 五要素", "top_k": 3}'

# 查看知识库统计
curl http://localhost:8904/stats
```

### A.4 端云协议调试

```bash
# 启动协议调试器
python -m ai_literacy.protocol_debugger

# 测试合规请求
curl -X POST http://localhost:8900/api/v1/edge-cloud/exchange \
  -H "Content-Type: application/json" \
  -d @test_request.json

# 查看 ZUP 审计日志
tail -f /var/log/ai-literacy/zup/audit.log

# 生成 ZUP 报告
python -m ai_literacy.zup.report
```

### A.5 性能监控

```bash
# 实时 NPU 利用率
watch -n 1 'curl -s http://localhost:8900/api/v1/npu-pool/status | jq'

# 本月云端成本
curl http://localhost:8900/api/v1/cost/monthly

# 缓存命中率
curl http://localhost:8900/api/v1/cache/stats
```

---

## 附录 B · 环境变量参考

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `V7_VERSION` | 7.0.0 | V7 版本号 |
| `V7_HOME` | /opt/ai-literacy | 安装目录 |
| `V7_MODELS` | /opt/ai-literacy/models | 模型目录 |
| `V7_LOGS` | /var/log/ai-literacy | 日志目录 |
| `V7_DATA` | /var/lib/ai-literacy | 数据目录 |
| `OPENAI_API_KEY` | - | OpenAI API Key |
| `ANTHROPIC_API_KEY` | - | Anthropic API Key |
| `QWEN_API_KEY` | - | 通义千问 API Key |
| `DEFAULT_LLM_PROVIDER` | openai | 默认云端 LLM |
| `ENABLE_CLOUD_FALLBACK` | true | 启用云端 Fallback |
| `GATEWAY_PORT` | 8900 | Gateway 端口 |
| `OCR_PORT` | 8901 | OCR 端口 |
| `ASR_PORT` | 8902 | ASR 端口 |
| `TTS_PORT` | 8903 | TTS 端口 |
| `RAG_PORT` | 8904 | RAG 端口 |
| `ANALYSIS_PORT` | 8905 | Analysis 端口 |
| `VLM_PORT` | 8906 | VLM 端口 |
| `LOCAL_LLM_PORT` | 8907 | 端侧 LLM 端口 |
| `NPU_DEVICE` | NPU | NPU 设备 |
| `OPENVINO_DEVICE` | NPU | OpenVINO 设备 |
| `LOG_LEVEL` | INFO | 日志级别 |
| `ZUP_RETENTION_DAYS` | 30 | ZUP 保留天数 |
| `CACHE_TTL` | 604800 | 缓存 TTL（7 天）|
| `MAX_CONCURRENT` | 50 | 最大并发数 |

---


---

> **重要提示**：
> 1. **数据安全第一**：V7 严格遵守"原始数据零上传"原则，所有 PII 数据都在端侧处理
> 2. **云端成本可控**：单任务 < $0.001，月度预算 < $10，远低于同类云端方案
> 3. **NPU 优化必备**：Intel 酷睿 Ultra 是 V7 端云协同的最佳硬件平台
> 4. **持续更新**：V7 将持续迭代（V7.1/V7.2 计划中），请关注官方发布

---

**🎉 V7 部署完成！** 现在你拥有了一个完整的端云协同 AI PC 教学操作系统。
