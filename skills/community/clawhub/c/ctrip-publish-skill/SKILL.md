---
name: 携程笔记全自动发布
version: 3.2.0
description: 携程内容中心全自动发布技能，支持从 Bing Images 搜索高清无版权图片、自动填写标题正文、自动上传图片、自动选择目的地、自动点击发布。适用于旅行攻略、美食推荐等图文笔记发布。
emoji: 🚄
---

# 携程笔记全自动发布技能

## 功能

- ✅ 自动打开携程发布页面
- ✅ 自动从 Bing Images 搜索高清无版权图片
- ✅ 自动填写标题和正文
- ✅ 自动上传图片（最多20张）
- ✅ 自动选择目的地
- ✅ 自动设置拍摄时间
- ✅ 自动添加话题标签
- ✅ 自动点击发布

## 使用场景

当用户说：
- "发携程笔记"
- "发布到携程"
- "全自动发布携程笔记"
- "帮我发到携程"
- "写一篇携程攻略"

## 技术实现

使用 OpenClaw 浏览器自动化 + CDP 协议：
1. 通过浏览器 CDP WebSocket 连接页面
2. 导航到携程内容中心发布页面
3. 使用 CDP setFileInputFiles 上传图片
4. 填写表单字段（标题、正文、地点）
5. 触发 React 合成事件更新状态
6. 点击发布按钮，处理确认弹窗

## 图片搜索功能

内置 Bing Images 搜索，可根据关键词自动下载高清图：
- 搜索关键词：故宫、长城、天坛、胡同、鸟巢、烤鸭等
- 自动过滤低分辨率图片
- 优先选择 1920x1080 以上的高清图
- 自动下载到 /tmp/openclaw/uploads/

## 依赖

- OpenClaw 浏览器工具
- Python 3 + websockets (用于 CDP)
- 网络访问 Bing Images

## 配置

无需 API Key，但需要：
1. 登录携程账号（首次需要扫码）
2. 图片上传到 /tmp/openclaw/uploads/

## 页面元素定位

### 携程发布页面关键元素

```
页面URL: https://we.ctrip.com/publish/publishPictureText

关键选择器:
- 图片上传: input[type="file"] (隐藏元素，需用CDP)
- 标题输入: [role="textbox"] (第一个)
- 正文编辑器: [role="combobox"] (第一个)
- 地点选择: .ant-select-selection-search-input
- 日期选择: input[placeholder*="日期"]
- 发布按钮: button (innerText = "发 布")
- 存草稿: button (innerText = "存草稿")
- 水印开关: .ant-switch
```

### 成功判断

- 发布成功后 URL 包含 `detail?articleId=`
- 或页面跳转到内容详情页

## 重要限制

1. **标题字数：必须少于20字**（不是≤20字）
   - 推荐 15-19 字
   - 超过会报错"标题字数需少于20个字"

2. **正文字数：建议 ≥60 字**
   - 更容易被评为优质内容

3. **图片数量：建议 3-20 张**
   - ≥3张有机会评为优质

4. **地点选择**：
   - 必须正确选择才能发布
   - 有时需要多次尝试才能选中

## CDP 图片上传示例

```python
import json, asyncio, websockets

async def upload_images(ws_url, files):
    async with websockets.connect(ws_url) as ws:
        # 获取DOM文档
        await ws.send(json.dumps({
            "id": 1,
            "method": "DOM.getDocument",
            "params": {"depth": -1}
        }))
        doc = json.loads(await ws.recv())
        
        # 查找file input
        await ws.send(json.dumps({
            "id": 2,
            "method": "DOM.querySelector",
            "params": {
                "nodeId": doc["result"]["root"]["nodeId"],
                "selector": "input[type='file']"
            }
        }))
        q = json.loads(await ws.recv())
        
        # 设置文件
        await ws.send(json.dumps({
            "id": 3,
            "method": "DOM.setFileInputFiles",
            "params": {
                "nodeId": q["result"]["nodeId"],
                "files": files  # 绝对路径列表
            }
        }))
```

## 使用示例

用户：帮我发一篇北京3天2晚的攻略到携程

AI：
1. 从 Bing Images 搜索北京景点高清图片
2. 下载故宫、长城、天坛等图片
3. 打开携程发布页面
4. 填写标题（<20字）："北京3天攻略！人均1500玩转帝都"
5. 填写正文行程内容（≥60字）
6. 上传下载的图片（3-20张）
7. 选择目的地"北京·中国"
8. 点击发布

## 常见问题

1. **地点选择失败**
   - 点击选择器展开下拉
   - 输入关键词后等待下拉出现
   - 点击匹配的选项

2. **发布按钮无反应**
   - 检查是否有必填项未填
   - 确认地点已正确选择
   - 查看页面是否显示错误提示

3. **图片上传失败**
   - 确认图片路径正确
   - 图片格式为 JPG/PNG
   - 单张图片 <10MB

## 快速链接

- 图文发布：https://we.ctrip.com/publish/publishPictureText
- 创作者后台：https://we.ctrip.com/publish/publishHome
- 内容管理：https://we.ctrip.com/publish/contentManagement