---
name: 抖音视频总结
description: 提取抖音播放页音频并通过自建服务转写字幕，随后总结内容、重点、观点或行动项。用户发送 douyin.com 链接、抖音分享文案，或要求总结、转写抖音视频时使用；不处理用户上传的本地视频文件。
---

# 抖音视频总结

从抖音播放页获取音频 URL，调用固定的转写 API 生成字幕，再按用户意图处理字幕。支撑服务会下载音频、临时上传为公有读 OSS 对象并把直链交给腾讯云，转写结束后删除；Skill 客户端不要自行下载视频或音频，不要安装或调用 ffmpeg。

## 选择链接

从用户消息中提取 `douyin.com` 或 `v.douyin.com` 链接，包括分享文案里的链接。若消息里有多个抖音链接，只处理文本中最后出现的一个，并简短说明已按规则选择最后一个。

没有抖音链接时，请用户补充链接。不要把普通网页链接或本地视频文件传给本技能的脚本。

## 获取播放页音频

1. 使用当前可用且允许执行页面 JavaScript 的浏览器打开所选链接；短链接跳转完成后，以最终播放页为准。
2. 等待视频开始加载。必要时点击播放，再在页面上下文执行以下函数：

```javascript
() => {
  const resources = performance.getEntriesByType('resource');
  const candidates = resources
    .map(entry => entry.name)
    .filter(url => /media-audio|audio.*byte|mime_type=audio|\.m4a(?:\?|$)|\.mp3(?:\?|$)/i.test(url));
  const audioUrl = candidates.at(-1) || null;
  const title = document.querySelector('[data-e2e="video-desc"]')?.textContent?.trim()
    || document.querySelector('h1')?.textContent?.trim()
    || document.title;
  const author = document.querySelector('[data-e2e="video-account-link"]')?.textContent?.trim()
    || document.querySelector('.author-name')?.textContent?.trim()
    || null;
  return { audioUrl, title: title || '未知标题', author: author || '未知作者' };
}
```

3. 若没有得到 `audioUrl`，等待 5 秒后重试，最多重试 3 次。仍失败时，检查页面是否被登录页、验证码或播放确认遮挡。需要用户操作时，明确告诉用户完成登录或验证，然后停止本次调用，不循环尝试。
4. 不要在回答、日志或命令输出中完整展示带签名的音频 URL。

## 调用转写服务

脚本位于本技能目录的 `scripts/transcribe.js`。在命令环境中传入页面提取结果：

```bash
DOUYIN_AUDIO_URL='<audioUrl>' \
DOUYIN_TITLE='<title>' \
DOUYIN_AUTHOR='<author>' \
node '<技能目录>/scripts/transcribe.js' '<用户消息中的最后一个抖音链接>'
```

脚本读取：

- `DOUYIN_AUDIO_URL`：必填，浏览器中提取的音频 URL。
- `DOUYIN_API_KEY`：必填，用户已有或新建的 API Key。
- `DOUYIN_TITLE`、`DOUYIN_AUTHOR`：可选。
- `DOUYIN_POLL_INTERVAL_MS`、`DOUYIN_TIMEOUT_MS`：仅在调试时可选。

转写 API 固定为 `https://calapi.ailuk.cn`，不要通过环境变量或用户输入覆盖。允许长视频转写持续一段时间。脚本会幂等提交并轮询，不要自行重复提交相同链接。

### 支撑服务异常

除“余额不足”外，只要转写接口请求失败、返回错误、响应无法解析、轮询超时或服务端任务失败，就立即停止本次调用。不要重试，不要改用其他转写服务，也不要向用户展示原始错误、错误码或技术细节；只告诉用户：

`支撑服务出问题了，不能继续了。`

### 缺少 API Key

停止转写并引导用户打开固定充值页，输入之前的 API Key 查询余额或按需创建新 Key：

`https://payhtml.ailuk.cn`

用户提供 Key 后，优先保存到平台安全凭据库并映射为 `DOUYIN_API_KEY`；无法使用凭据库时，才写入仅当前用户可读的本地环境配置。不要在回答、日志、报错或命令中回显完整 Key。

### 余额不足

当脚本返回退出码 `2` 或错误码 `INSUFFICIENT_BALANCE` 时，引导用户打开 `https://payhtml.ailuk.cn` 并停止。用户确认充值完成后，对原任务只重试一次；再次失败则报告结果并停止。不要代用户付款，不要循环轮询余额。

## 使用字幕回答

转写成功后，先提供视频标题、作者、时长、扣费和一段简短总结。随后按用户原始目的处理字幕：

- “总结”：给出核心结论和 3–7 个要点。
- “找重点”：保留关键事实、数字、观点、争议和结论，并附对应时间戳。
- “做笔记”：按主题组织，去掉口头重复，但不要引入字幕外事实。
- “行动项”：提炼可执行动作、负责人或期限；字幕未说明的字段标为“未提及”。
- “要原文/字幕”：返回可读的分段字幕；内容很长时先给摘要，再询问是否展开全文。

字幕可能有同音字或专有名词错误。影响结论时明确标记不确定项，不凭空修正。用户未指定输出形式时，默认使用“简短总结 + 重点列表 + 可继续追问的方向”，不要只倾倒完整字幕。
