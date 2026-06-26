# Coze 工作流列表参考

## 工作流汇总

| 序号 | 工作流ID | 用途说明 | 链接 |
|:---:|:---|:---|:---|
| 1 | 7610360135081295918 | 邮件触发工作流 - 接收用户邮箱，触发特定业务逻辑 | [查看](https://www.coze.cn/space/7555350866765545515/project-ide/7610360135081295918) |

---

## 详情说明

### 1. 邮件触发工作流 (7610360135081295918)

- **用途**：接收用户提交的邮箱地址，触发后续业务处理
- **输入参数**：需要传入 `input` 参数，格式为字符串（如 "姓名等信息，联系邮箱: xxx@email.com"）
- **调用方式**：POST 请求到 `/api/proxy/coze`，传递 `workflow_id` 和 `parameters`

---

## 调用示例

### 后端代理（Node.js）

```javascript
const COZE_API_URL = 'https://api.coze.cn/v1/workflow/run';
const COZE_AUTH_TOKEN = 'Bearer 你的服务令牌';

app.post('/api/proxy/coze', async (req, res) => {
  const { workflow_id, parameters } = req.body;
  const response = await fetch(COZE_API_URL, {
    method: 'POST',
    headers: {
      'Authorization': COZE_AUTH_TOKEN,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ workflow_id, parameters: parameters || {} })
  });
  const data = await response.json();
  res.status(response.status).json(data);
});
```

### Python 脚本调用

```bash
python3 run_workflow.py 7610360135081295918 "姓名: 张三, 邮箱: test@example.com"
```