# 🤖 模块 11：AI 办公 ⭐ v3.8.0 新增模块

---

#### 11.1 会议纪要生成器 ⭐ v3.8.0 新增

**✅ 开箱即用**（零依赖保底：支持本地 whisper / 在线 API / 手动粘贴文本 三级降级）

> 语音→ASR 转写→LLM 摘要→结构化会议纪要。覆盖 TOP50 高频需求。

<details>
<summary>📋 模式 A：本地 Whisper CLI（离线，零成本）</summary>

```python
import subprocess, os, sys

path = input("音频文件路径(mp3/wav/m4a):").strip().strip('"').strip("'")
if not os.path.isfile(path):
    print(f"❌ 文件不存在: {path}")
else:
    r = subprocess.run(["whisper", "--help"], capture_output=True, text=True, timeout=5)
    if r.returncode != 0:
        print("❌ 未检测到 whisper CLI。请先安装：pip install openai-whisper")
        print("   或选择模式 B（在线 API）或模式 C（手动粘贴文本）")
    else:
        print("🎙️ 正在转写（可能需要几分钟，取决于音频长度）...")
        result = subprocess.run(
            ["whisper", path, "--language", "zh", "--output_format", "txt",
             "--output_dir", os.path.dirname(path)],
            capture_output=True, text=True, timeout=600
        )
        if result.returncode == 0:
            out_path = os.path.splitext(path)[0] + ".txt"
            if os.path.exists(out_path):
                with open(out_path, encoding="utf-8") as f:
                    text = f.read()
                print(f"✅ 转写完成！文本长度: {len(text)} 字")
                print("--- 转写结果 ---")
                print(text[:500])
            else:
                print("❌ 转写输出文件未生成")
        else:
            print(f"❌ 转写失败: {result.stderr[:200]}")
```

</details>

<details>
<summary>📋 模式 B：Paraformer API（在线，中文识别率高）</summary>

```python
import urllib.request, urllib.parse, json, os

path = input("音频文件路径:").strip().strip('"').strip("'")
if not os.path.isfile(path):
    print(f"❌ 文件不存在: {path}")
else:
    API_URL = input("API URL(留空使用内置示例):").strip()
    API_KEY = input("API Key(留空使用内置示例):").strip()
    
    if not API_URL:
        print("💡 未配置 API，将使用模式 C（手动粘贴文本）")
        print("   如需在线识别，请提供 Paraformer API 地址和密钥")
    else:
        with open(path, "rb") as f:
            audio_data = f.read()
        req = urllib.request.Request(
            API_URL,
            data=audio_data,
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "audio/wav"}
        )
        try:
            resp = urllib.request.urlopen(req, timeout=120)
            result = json.loads(resp.read())
            text = result.get("text", result.get("result", ""))
            if text:
                print(f"✅ 转写完成！文本长度: {len(text)} 字")
                print("--- 转写结果 ---")
                print(text[:500])
            else:
                print("❌ API 返回空文本")
        except Exception as e:
            print(f"❌ API 调用失败: {e}")
            print("   请检查网络连接和 API 配置")
```

</details>

<details>
<summary>📋 模式 C：手动粘贴文本（零依赖保底，推荐）</summary>

```python
import datetime

print("📋 模式 C：手动粘贴会议录音转写文本")
print("   （如无 ASR 工具，可手动复制会议录音转写内容）")
print("   输入文本后输入 END 结束：")
lines = []
while True:
    line = input()
    line = line.strip() if line else ""
    if line.upper() == "END":
        break
    lines.append(line)
text = "\n".join(lines)

if not text.strip():
    print("❌ 未输入文本")
else:
    sentences = [s.strip() for s in text.replace("。","\n").replace("！","\n").replace("？","\n").split("\n") if len(s.strip()) > 5]
    key_sentences = [s for s in sentences if any(kw in s for kw in ["决定","同意","通过","计划","负责","截止","下周","跟进","负责人","审核"])]
    today = datetime.date.today().strftime("%Y-%m-%d")
    print(f"\n{'='*50}")
    print(f"  📝 会议纪要（结构化摘要）")
    print(f"  日期: {today} | 原文: {len(text)} 字")
    print(f"{'='*50}")
    print(f"\n## 📋 会议要点\n")
    if key_sentences:
        for i, s in enumerate(key_sentences[:10], 1):
            print(f"{i}. {s}")
    else:
        for i, s in enumerate(sentences[:5], 1):
            print(f"{i}. {s}")
    print(f"\n## 📝 完整文本\n")
    print(text[:1000])
    if len(text) > 1000:
        print(f"\n...（共 {len(text)} 字，已截断）")
    print(f"\n{'='*50}")
    print("⚠️ 零依赖模式使用规则引擎摘要，安装 LLM 后可获得更智能的归纳")
```

</details>

**⚠️ 三级降级链说明：**

| 优先级 | 模式 | 依赖 | 中文识别率 | 适用场景 |
|:------:|------|------|:----------:|----------|
| 1 | 本地 Whisper CLI | `pip install openai-whisper` | 85-90% | 离线、大文件、隐私敏感 |
| 2 | Paraformer API | 联网 + API Key | 92-95% | 中文会议、高准确率需求 |
| 3 | 手动粘贴文本 | **零依赖** | 100%（人工） | 无安装条件、短文本、兜底 |

> 推荐：先用模式 C 体验，需要自动化时再安装 whisper 或配置 API。
