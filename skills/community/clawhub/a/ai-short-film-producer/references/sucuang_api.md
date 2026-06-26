# 速创API 接口文档与踩坑经验

## 平台信息

- **平台地址**: （注册后获取）
- **文档中心**: （注册后获取）
- **API Key获取**: 注册登录后进入控制台获取

## 通用鉴权方式

**推荐方式 — Authorization Header（不带Bearer前缀）：**
```python
HEADERS = {
    "Authorization": "你的API_KEY",
    "Content-Type": "application/json"
}
```

**❌ 不要用URL参数传key：**
```python
# 会返回403，不要这样用
requests.get("平台API地址/api/xxx?key=你的API_KEY")
```

---

## 1. Grok Imagine 视频生成

### 接口信息
- **接口**: POST `/api/async/video/grok_imagine`
- **价格**: 按秒计费（具体见平台）
- **点数**: 5点/秒
- **免费额度**: 无
- **QPS限制**: 100次/秒
- **每日限制**: 付费用户不限制

### 请求参数
```json
{
  "prompt": "英文描述效果更稳定，包含场景、光线、构图、镜头运动",
  "duration": 10,
  "style": "cinematic"
}
```

### 结果查询
- **接口**: `GET /api/async/detail?id=xxx`
- **轮询策略**: 每5秒查询一次
- **状态码**: status=2 表示完成，status=0/1 表示处理中
- **返回内容**: 包含视频下载URL

### 批量生成策略
```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def submit_shot(shot):
    # 提交生成任务
    resp = requests.post(url, headers=HEADERS, json=params)
    task_id = resp.json()["data"]["id"]
    # 轮询直到完成
    while True:
        result = requests.get(f"{BASE}/detail?id={task_id}", headers=HEADERS)
        if result.json()["data"]["status"] == 2:
            return download_video(result.json()["data"]["video_url"])
        time.sleep(5)

# 批量25个镜头同时提交
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(submit_shot, shot) for shot in SHOTS]
    for future in as_completed(futures):
        results.append(future.result())
```

### 踩坑经验
- Sora2接口（sora2/video）已不可用，持续返回400错误，全部使用Grok Imagine
- 英文Prompt比中文Prompt效果更稳定
- 平均重试3次才能获得满意结果
- 生成耗时约30-60秒/个

---

## 2. TTS配音生成

### 接口信息
- **接口**: `POST /api/async/audio_tts`
- **价格**: 按字计费（具体见平台）
- **返回格式**: tar包（需解压获取mp3）

### 请求参数（重要：扁平JSON）
```json
{
  "text": "台词内容",
  "voice_id": "male-qn-jingying",
  "speed": 1.0
}
```

### 可用音色列表
| 音色ID | 描述 | 适用角色 |
|--------|------|---------|
| male-qn-jingying | 精英青年男声 | 旁白、汪淼、常伟思 |
| male-qn-badao | 霸道男声 | 史强 |
| male-qn-daxuesheng | 大学生男声 | 研究员 |
| male-chunhou | 醇厚男声 | 长辈角色 |
| junlang_nanyou | 俊朗男声 | 潘寒 |
| female-chengshu | 成熟女声 | 申玉菲 |
| female-shaonv | 少女音 | 杨冬 |

### 踩坑经验（重要）
1. **❌ 不要传 format 参数** — 会报500"存在未绑定的参数"
2. **❌ 不要嵌套参数** — 不要写成 `{"model":"audio_tts","params":{...}}`，直接扁平JSON
3. **✅ 状态码判断** — 用 `status == 2` 判断完成，不要用字符串 `"completed"`
4. **⚠️ 部分任务会卡住** — status一直=0，重试可换到不同IP节点
5. **✅ 返回tar包** — 需要用 `tarfile` 解压获取mp3文件

### TTS生成代码模板
```python
import requests, time, tarfile, io

def generate_tts(text, voice_id, output_path):
    payload = {"text": text, "voice_id": voice_id, "speed": 1.0}
    resp = requests.post(f"{BASE}/api/async/audio_tts", headers=HEADERS, json=payload)
    task_id = resp.json()["data"]["id"]

    while True:
        result = requests.get(f"{BASE}/api/async/detail?id={task_id}", headers=HEADERS)
        data = result.json()["data"]
        if data["status"] == 2:  # 完成
            audio_url = data["audio_url"]
            audio_resp = requests.get(audio_url)
            tar = tarfile.open(fileobj=io.BytesIO(audio_resp.content))
            for member in tar.getmembers():
                if member.name.endswith('.mp3'):
                    f = tar.extractfile(member)
                    with open(output_path, 'wb') as out:
                        out.write(f.read())
            return
        elif data["status"] == -1:  # 失败
            raise Exception(f"TTS failed: {data}")
        time.sleep(3)
```

---

## 3. 数字人视频生成

### 接口信息
- **接口**: `POST /api/async/video_digital_humans`
- **价格**: 按次计费

### 请求参数
```json
{
  "audio_url": "公网可访问的音频URL",
  "video_url": "公网可访问的视频URL"
}
```

### 注意事项
- 音频和视频URL必须公网可访问
- 推荐搭配云存储服务存储素材

---

## 4. 云存储配置（素材存储）

如需存储视频和音频文件，推荐使用云存储服务：
- 腾讯云COS
- 阿里云OSS
- AWS S3

请根据实际需求配置您自己的云存储凭证。

---

## 5. 其他可用模型

速创API平台还提供以下模型（价格以平台实际为准）：
- 文生图模型（多种）
- 视频编辑模型
- 语音识别
- 大语言模型对话

具体价格请查看平台定价页面。