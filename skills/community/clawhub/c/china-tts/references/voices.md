# 音色完整列表

来源：硅基流动官方文档 2.1 系统预置音色

## CosyVoice2-0.5B 系统预置音色（8种）

调用格式：`"voice": "FunAudioLLM/CosyVoice2-0.5B:{音色名}"`

### 男声

| 音色名 | 风格 | voice 参数值 |
|---|---|---|
| alex | 沉稳男声 | `FunAudioLLM/CosyVoice2-0.5B:alex` |
| benjamin | 低沉男声 | `FunAudioLLM/CosyVoice2-0.5B:benjamin` |
| charles | 磁性男声 | `FunAudioLLM/CosyVoice2-0.5B:charles` |
| david | 欢快男声 | `FunAudioLLM/CosyVoice2-0.5B:david` |

### 女声

| 音色名 | 风格 | voice 参数值 |
|---|---|---|
| anna | 沉稳女声 | `FunAudioLLM/CosyVoice2-0.5B:anna` |
| bella | 激情女声 | `FunAudioLLM/CosyVoice2-0.5B:bella` |
| claire | 温柔女声 | `FunAudioLLM/CosyVoice2-0.5B:claire` |
| diana | 欢快女声 | `FunAudioLLM/CosyVoice2-0.5B:diana` |

在线试听：https://soundcloud.com/siliconcloud/sets/siliconcloud-online-voice

---

## MOSS-TTSD-v0.5 系统预置音色

调用格式：`"voice": "fnlp/MOSS-TTSD-v0.5:{音色名}"`

| 音色名 | voice 参数值 |
|---|---|
| alex | `fnlp/MOSS-TTSD-v0.5:alex` |
| anna | `fnlp/MOSS-TTSD-v0.5:anna` |
| bella | `fnlp/MOSS-TTSD-v0.5:bella` |
| benjamin | `fnlp/MOSS-TTSD-v0.5:benjamin` |
| charles | `fnlp/MOSS-TTSD-v0.5:charles` |
| claire | `fnlp/MOSS-TTSD-v0.5:claire` |
| david | `fnlp/MOSS-TTSD-v0.5:david` |
| diana | `fnlp/MOSS-TTSD-v0.5:diana` |

---

## 自定义音色（声音克隆）

需要实名认证，上传参考音频后获得 URI。

URI 格式：`speech:{customName}:{用户ID}:{随机字符串}`

使用时直接将 URI 填入 voice 参数：
```
"voice": "speech:my-voice:cm04pf7az00061413w7kz5qxs:mjtkgbyuunvtybnsvbxd"
```

### 参考音频要求（官方最佳实践）

```
时长：8~10 秒为佳，不超过 30 秒
人数：仅限单一说话人
质量：
  - 吐字清晰，音量稳定
  - 无背景噪音，无回声
  - 停顿短暂（建议 0.5 秒以内）
格式：mp3 / wav / pcm / opus
  - 推荐 192kbps 以上的 mp3
```

### 查看已上传的自定义音色

```bash
curl --location 'https://api.siliconflow.cn/v1/audio/voice/list' \
  --header "Authorization: Bearer $SILICONFLOW_API_KEY"
```

### 删除自定义音色

```bash
curl --location 'https://api.siliconflow.cn/v1/audio/voice/deletions' \
  --header "Authorization: Bearer $SILICONFLOW_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{"uri": "speech:your-voice-name:xxxxx:xxxxx"}'
```

---

## 场景推荐音色

```
新闻播报 / 正式朗读    → alex（沉稳男声）或 anna（沉稳女声）
有声书 / 故事朗读      → charles（磁性男声）或 claire（温柔女声）
活泼内容 / 短视频配音  → david（欢快男声）或 diana（欢快女声）
播客 / 深度内容        → benjamin（低沉男声）或 bella（激情女声）
双人播客对话           → MOSS-TTSD，S1用charles，S2用claire
```
