# 百度文档解析 API 错误码参考

## 通用错误

### 认证相关错误

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|---------|------|----------|
| 1 | Unknown error | 未知错误 | 重试请求，持续出现请联系技术支持 |
| 2 | Service temporarily unavailable | 服务暂不可用 | 重试请求，持续出现请联系技术支持 |
| 3 | Unsupported openapi method | API 接口不存在 | 检查 URL 是否正确，去除非英文字符 |
| 4 | Open api request limit reached | 集群超限额 | 重试请求，持续出现请联系技术支持 |
| 6 | No permission to access data | 无 API 访问权限 | 在百度云控制台开通该 API 权限 |
| 14 | IAM Certification failed | IAM 认证失败 | 检查签名生成方式或改用 AK/SK |
| 17 | Open api daily request limit reached | 日配额超限 | 购买额度或等待次日重置 |
| 18 | Open api qps request limit reached | QPS 超限 | 降低请求频率 |
| 19 | Open api total request limit reached | 总量配额超限 | 购买额外配额 |
| 100 | Invalid parameter | access_token 无效 | 重新获取 access_token |
| 110 | Access token invalid or no longer valid | access_token 无效 | token 有效期 30 天，重新获取 |
| 111 | Access token expired | access_token 过期 | token 有效期 30 天，重新获取 |

### 文件相关错误

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|---------|------|----------|
| 216200 | empty file or fileurl | 文件或 URL 为空 | 提供 file_data 或 file_url |
| 216201 | file format error | 文件格式不支持 | 使用支持的格式（PDF、Word、Excel 等） |
| 216202 | file size error | 文件大小超限 | 缩减文件大小（file_data ≤ 50MB，file_url PDF ≤ 300MB） |

### 任务处理错误

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|---------|------|----------|
| 282000 | internal error | 任务处理失败 | 重试或联系技术支持 |
| 282001 | template not found | 合同类型未找到 | 检查合同类型名称 |
| 282003 | missing parameters | 缺少必要参数 | 检查必填参数 |
| 282005 | quota exceed error | 额度不足 | 申请增加配额 |
| 282006 | check user auth error | 用户权限校验失败 | 验证用户权限 |
| 282007 | task not exist, please check task id | 任务不存在 | 检查 task_id 是否正确 |
| 282018 | Service busy | 服务繁忙 | 降低请求频率 |

### URL 相关错误

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|---------|------|----------|
| 282111 | url format illegal | URL 格式不合法 | 检查 URL 格式 |
| 282112 | url download timeout | URL 下载超时 | 检查 URL 是否可访问 |
| 282113 | url response invalid | URL 响应无效 | 检查 URL 返回内容是否正确 |
| 282114 | url size error | URL 长度超过 1024 字节 | 缩短 URL |

### 参数错误

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|---------|------|----------|
| 283016 | parameters value error | 参数值无效 | 检查参数格式和取值 |

## 错误响应格式

```json
{
  "log_id": "13665091038742503867108513247688",
  "error_code": "282007",
  "error_msg": "task not exist, please check task id",
  "result": "null"
}
```

## 错误处理策略

### 重试策略

| 错误类型 | 错误码 | 建议处理方式 |
|---------|--------|-------------|
| 瞬时错误 | 1, 2, 4, 282000, 282018 | 指数退避重试 |
| 认证错误 | 100, 110, 111 | 重新获取 access_token |
| 配额错误 | 17, 18, 19, 282005 | 等待或购买额外配额 |
| 参数错误 | 216200, 216201, 282003, 283016 | 修正参数后重试 |
| URL 错误 | 282111, 282112, 282113, 282114 | 检查并修正 URL |

### 指数退避重试示例

```python
import time

def retry_with_backoff(func, max_retries=3):
    for i in range(max_retries):
        try:
            return func()
        except Exception as e:
            if i == max_retries - 1:
                raise
            wait_time = 2 ** i  # 1s, 2s, 4s
            time.sleep(wait_time)
```

### Token 刷新示例

```python
def ensure_valid_token(client):
    try:
        client.query_task("test-task-id")
    except Exception as e:
        if "110" in str(e) or "111" in str(e):
            client.access_token = client._fetch_auth_credential()
```

## 获取帮助

- [提交工单](https://ticket.bce.baidu.com/?_=1648086674827&fromai=1#/ticket/create~productId=96&questionId=1306&channel=2)
- [权限诊断工具](https://console.bce.baidu.com/tools/#/aiInterfacePermissions)
- [百度云控制台](https://console.bce.baidu.com/ai/)
