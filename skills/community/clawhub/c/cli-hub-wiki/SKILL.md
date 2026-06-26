---
name: cli-hub-wiki
version: 1.0.0
description: CLI-Hub工具箱 - 100+ CLI工具一键安装。浏览器自动化、视频编辑、知识管理、AI模型、云服务等。源自HKUDS CLI-Anything项目。
keywords: [cli,automation,browser,video,knowledge,management,ollama,clihub]
---

# CLI-Hub 工具箱

**来源：** HKUDS CLI-Anything  
**安装：** `pip install cli-anything-hub`  
**命令：** `cli-hub`

---

## 核心命令

```bash
cli-hub list          # 查看所有可用CLI
cli-hub search <词>    # 搜索CLI
cli-hub install <名>   # 安装CLI
cli-hub info <名>      # 查看CLI详情
cli-hub launch <名>   # 运行CLI
cli-hub update <名>    # 更新CLI
cli-hub uninstall <名> # 卸载CLI
```

---

## 分类CLI列表

### 🌐 浏览器自动化
| CLI | 说明 | 安装 |
|-----|------|------|
| browser | Chrome自动化 via DOMShell | `cli-hub install browser` |
| clibrowser | 零依赖AI浏览器CLI | `cli-hub install clibrowser` |
| safari | macOS Safari自动化 | `cli-hub install safari` |

### 🎬 视频处理
| CLI | 说明 | 安装 |
|-----|------|------|
| kdenlive | 视频编辑渲染 via melt | `cli-hub install kdenlive` |
| shotcut | 视频编辑 via ffmpeg | `cli-hub install shotcut` |
| openscreen | 屏幕录制编辑 | `cli-hub install openscreen` |
| videocaptioner | AI视频字幕生成 | `cli-hub install videocaptioner` |

### 📚 知识管理
| CLI | 说明 | 安装 |
|-----|------|------|
| obsidian | Obsidian笔记管理 | `cli-hub install obsidian` |
| mubu | 知识大纲工具 | `cli-hub install mubu` |
| zotero | Zotero文献管理 | `cli-hub install zotero` |

### 🤖 AI模型
| CLI | 说明 | 安装 |
|-----|------|------|
| ollama | 本地LLM推理管理 | `cli-hub install ollama` |
| novita | Novita AI API访问 | `cli-hub install novita` |
| comfyui | AI图像生成工作流 | `cli-hub install comfyui` |

### ☁️ 云服务
| CLI | 说明 | 安装 |
|-----|------|------|
| aws | AWS云服务管理 | `cli-hub install aws` |
| cloudalyzer | 云成本分析 | `cli-hub install cloudalyzer` |

### 🔧 自动化
| CLI | 说明 | 安装 |
|-----|------|------|
| n8n | 工作流自动化 | `cli-hub install n8n` |
| pm2 | Node.js进程管理 | `cli-hub install pm2` |

### 🎨 设计
| CLI | 说明 | 安装 |
|-----|------|------|
| blender | 3D建模动画渲染 | `cli-hub install blender` |
| drawio | 图表创建导出 | `cli-hub install drawio` |
| mermaid | Mermaid图表 | `cli-hub install mermaid` |
| sketch | Sketch设计文件 | `cli-hub install sketch` |

### 🎮 游戏
| CLI | 说明 | 安装 |
|-----|------|------|
| godot | Godot游戏引擎 | `cli-hub install godot` |
| slay_the_spire_ii | 杀戮尖塔2自动化 | `cli-hub install slay_the_spire_ii` |

### 📊 数据
| CLI | 说明 | 安装 |
|-----|------|------|
| chromadb | 向量数据库 | `cli-hub install chromadb` |
| eth2-quickstart | 以太坊节点部署 | `cli-hub install eth2-quickstart` |

---

## 使用示例

### 安装浏览器自动化
```bash
cli-hub install browser
```

### 搜索视频相关CLI
```bash
cli-hub search video
```

### 查看Obsidian详情
```bash
cli-hub info obsidian
```

### 运行Ollama
```bash
cli-hub launch ollama --help
```

---

## 适用场景

| 任务 | 推荐CLI |
|------|---------|
| 网页截图/爬取 | `browser`, `clibrowser` |
| 视频字幕生成 | `videocaptioner` |
| 笔记管理 | `obsidian` |
| 本地LLM | `ollama` |
| AI图像生成 | `comfyui` |
| 云成本分析 | `cloudalyzer` |
| 3D建模 | `blender` |
| 工作流自动化 | `n8n` |

---

## 安装状态

CLI-Hub已安装在: `/usr/local/bin/cli-hub`

查看所有CLI:
```bash
cli-hub list
```

搜索特定CLI:
```bash
cli-hub search <关键词>
```

---

## 对比：自己写 vs CLI-Hub

| 自己写 | CLI-Hub |
|--------|---------|
| 从零开始 | 100+现成工具 |
| 需维护代码 | 自动更新 |
| 功能有限 | 社区贡献 |
| 耗时 | 一键安装 |

---

*Powered by HKUDS CLI-Anything | Updated: 2026-04-17*
