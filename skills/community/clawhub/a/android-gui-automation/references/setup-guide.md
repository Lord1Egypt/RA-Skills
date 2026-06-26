# Android GUI Automation - 参考文档

## 快速开始清单

### 手机端准备

- [ ] 开启「开发者选项」→「USB 调试」
- [ ] （可选）开启「无线调试」获得 IP:PORT
- [ ] 安装 Tasker 或 MacroDroid（方案B需要）
- [ ] 安装 Termux

### Termux 端安装

```bash
pkg update && pkg upgrade
pkg install python python-pip
pip install uiautomator2 requests schedule
python -m uiautomator2 init
```

### 测试连接

```bash
# 在电脑上用 ADB 连接（USB 或无线）
adb connect <手机IP>:5555

# 或在 Termux 里直接运行
python3 -c "import uiautomator2 as u2; d = u2.connect(); print(d.info)"
```

## 常见 APP 包名

| APP | 包名 |
|-----|------|
| 淘宝 | `com.taobao.taobao` |
| 京东 | `com.jingdong.app.mall` |
| 拼多多 | `com.xunmeng.pinduoduo` |
| 微信 | `com.tencent.mm` |
| 美团 | `com.sankuai.meituan` |
| 抖音 | `com.ss.android.ugc.aweme` |
| 小红书 | `com.xingin.xhs` |

## 元素定位方法

```python
# 方法1: 文本定位（最常用）
d(text="搜索").click()

# 方法2: 描述内容定位
d(description="搜索").click()

# 方法3: XPath（最灵活）
d.xpath('//android.widget.TextView[@text="搜索"]').click()

# 方法4: 类名+索引
d(className="android.widget.EditText", instance=0).set_text("iPhone")

# 方法5: 坐标点击
d.click(540, 960)
```

## uiautomator2 截图 & OCR

```python
# 截图
d.screenshot("screen.png")

# 读取屏幕上所有文字（需联网 OCR）
# 可用百度/腾讯 OCR API，或用 pytesseract 本地识别

# 读取 UI XML 结构
xml = d.dump_xml()
print(xml)
```

## 异常处理

```python
try:
    d(text="搜索").click()
except Exception as e:
    print(f"点击失败: {e}")
    # 备选：用坐标点击
    d.click(540, 960)
```

## 价格提醒对接

Telegram Bot 通知格式：

```bash
# 测试通知
curl -X POST "https://api.telegram.org/bot<TOKEN>/sendMessage" \
  -d "chat_id=<CHAT_ID>" \
  -d "text=测试消息" \
  -d "parse_mode=Markdown"
```
