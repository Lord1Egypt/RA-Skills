# 使用示例

## 场景一：每日数据同步

假设你有一个 RPA 应用，每天需要从数据库同步数据：

### 配置
```json
{
  "url": "https://api-rpa.bazhuayu.com/api/v1/bots/webhooks/YOUR_WEBHOOK_ID/invoke",
  "key": "YOUR_SECRET_KEY",
  "paramNames": ["日期", "数据源"],
  "defaultParams": {
    "日期": "2026-03-05",
    "数据源": "main_db"
  }
}
```

### 运行
```bash
# 使用默认参数
python3 bazhuayu-webhook.py run

# 指定日期和数据源
python3 bazhuayu-webhook.py run --日期=2026-03-06 --数据源=backup_db
```

---

## 场景二：订单处理

假设你有一个订单处理 RPA，需要传递订单号和收货地址：

### 配置
```json
{
  "url": "https://api-rpa.bazhuayu.com/api/v1/bots/webhooks/YOUR_ID/invoke",
  "key": "YOUR_KEY",
  "paramNames": ["订单号", "收货地址"],
  "defaultParams": {
    "订单号": "",
    "收货地址": ""
  }
}
```

### 运行
```bash
python3 bazhuayu-webhook.py run --订单号=ORD20260305001 --收货地址=北京市朝阳区 xx 路 xx 号
```

---

## 场景三：定时任务

设置每天 8 点自动运行：

### 1. 配置默认参数
```json
{
  "url": "https://api-rpa.bazhuayu.com/api/v1/bots/webhooks/YOUR_ID/invoke",
  "key": "YOUR_KEY",
  "paramNames": ["A", "B"],
  "defaultParams": {
    "A": "默认值 A",
    "B": "默认值 B"
  }
}
```

### 2. 添加定时任务
```bash
crontab -e
```

添加：
```
0 8 * * * /path/to/bazhuayu-webhook/run_daily.sh
```

---

## 场景四：多参数传递

如果 RPA 应用有多个参数：

### 配置
```json
{
  "url": "https://api-rpa.bazhuayu.com/api/v1/bots/webhooks/YOUR_ID/invoke",
  "key": "YOUR_KEY",
  "paramNames": ["用户名", "密码", "操作类型", "备注"],
  "defaultParams": {
    "用户名": "admin",
    "密码": "123456",
    "操作类型": "login",
    "备注": ""
  }
}
```

### 运行
```bash
python3 bazhuayu-webhook.py run --用户名=test --密码=654321 --操作类型=logout
```

---

## 场景五：10 个以上参数

支持任意数量的参数：

### 配置
```json
{
  "url": "https://api-rpa.bazhuayu.com/api/v1/bots/webhooks/YOUR_ID/invoke",
  "key": "YOUR_KEY",
  "paramNames": [
    "参数 1", "参数 2", "参数 3", "参数 4", "参数 5",
    "参数 6", "参数 7", "参数 8", "参数 9", "参数 10"
  ],
  "defaultParams": {
    "参数 1": "值 1",
    "参数 2": "值 2",
    "参数 3": "100",
    "参数 4": "true",
    "参数 5": "2026-03-05",
    "参数 6": "值 6",
    "参数 7": "值 7",
    "参数 8": "值 8",
    "参数 9": "值 9",
    "参数 10": "值 10"
  }
}
```

### 运行
```bash
# 只修改需要改变的参数
python3 bazhuayu-webhook.py run --参数 1=新值 1 --参数 3=500 --参数 10=新值 10
```
