# coze-image

扣子(Coze) Seedream 4.5 图片生成工具

## 依赖

```bash
pip install requests
```

## 配置

编辑 `coze_image.py`，修改 CONFIG 中的配置：

```python
CONFIG = {
    "api_token": "YOUR_COZE_API_TOKEN",    # 你的 Coze API Token
    "workflow_id": "YOUR_WORKFLOW_ID",    # 图片生成工作流 ID
    "api_url": "https://api.coze.cn/v1/workflow/run"
}
```

## 获取配置

1. **API Token**: 登录 https://www.coze.cn → API管理 → 授权 → 创建Token
2. **Workflow ID**: 在工作流URL中找到，如 `workflow_id=7644576791978033769`

## 使用

```bash
# 生成图片
python coze_image.py generate "a cute cat"

# 生成并保存到本地
python coze_image.py generate "a sunset" -o ./image.png
```

## 参数说明

- `input`: 图片描述提示词（必填）
- 工作流返回图片 URL 格式: `https://s.coze.cn/t/xxx/`