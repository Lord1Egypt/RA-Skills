# 故障排查

## M4 黑屏 / 最后几秒黑帧

**原因**: 素材总时长 < storyboard 场景所需时长  
**检查**: 每个素材至少 10s，总素材时长应 > TTS 时长 + 3s  
**修复**: 
- 降低 `workflow.storyboard_padding`（默认3→1）
- 用更长素材替换短素材（<7s 素材已自动过滤）
- 减少 M2 storyboard 场景数

## TTS 超长

**原因**: 口播词数 > `video.max_words`(120)  
**修复**: 
- `video.max_words` 已自动截断到最近句号
- 或手动删减口播文案

## DeepSeek API 超时 / 连接拒绝

**原因**: API Key 失效或网络问题  
**修复**:
1. 检查 `DEEPSEEK_API_KEY` 环境变量
2. 检查 `config.yaml` → `api.deepseek.api_key`
3. 尝试切换 `fallback_model: deepseek-v4-flash`

## M3 素材缺口

**原因**: `library_dir` 下没有匹配场景的素材  
**修复**:
1. 检查素材文件名是否包含场景中文名
2. 检查 `EN_TO_CN_SCENE` 映射是否覆盖了英文场景
3. 补充素材到 `library/竖屏/` 目录

## M6 发布失败

**原因**: Metricool Token 过期或 API 不通  
**修复**:
1. 重新获取 Token：`curl -H "X-Mc-Auth: {token}" https://app.metricool.com/api/v2/settings/brands?userId={uid}`
2. 检查 `METRICOOL_TOKEN` 和 `METRICOOL_USER_ID`

## Chrome 内存泄漏

**原因**: 每条视频开 Chrome 不关  
**修复**: 已内置 `cleanup_chrome()`（pkill Chrome），每条前后自动清

## 环境安装

```bash
# Python 依赖
pip install openai pyyaml requests

# 系统工具
brew install ffmpeg cwebp

# TTS（二选一）
pip install ChatTTS    # 推荐（开源高质量）
pip install edge-tts   # 备用（微软 Edge）
```
