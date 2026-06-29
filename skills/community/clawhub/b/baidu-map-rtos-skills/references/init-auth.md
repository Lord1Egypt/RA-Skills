# 鉴权、初始化与 Canvas 适配

## 初始化顺序

```
BaseApi::SetPackageName
→ AuthLicenseApi::SetAk → RequestLicense → Authenticate（异步）
→ MapComponentApi::MarkComponentAlive(true)
→ SetCanvas（先调 MapCanvasImpl::setCanvas(platformCanvasContext)）
→ SetUIThreadFunc
→ InitMap()
→ RequestRender()
→ ... 业务逻辑 ...
→ MarkComponentAlive(false)
```

完整可运行代码见 [demo.md § main 初始化全流程](demo.md)。

---

## Canvas 适配层要点

Canvas 接口实现要求与绑定流程见 [adapter-build.md](adapter-build.md)。

`SetUIThreadFunc`：注册 SDK 数据刷新回调，SDK 内部渲染数据更新时触发，应用在回调里调用 `RequestRender` 拉取新数据；回调本身在应用的 UI/渲染线程执行。

---

## 首轮联调验收清单

1. `Authenticate` 成功
2. `MarkComponentAlive(true)`
3. `SetCanvas` + `SetSize`
4. `SetUIThreadFunc`
5. `InitMap()`
6. UI 线程收到渲染请求并调用 `RequestRender`
7. 可见底图背景、矢量线、POI 文本/图标
8. 拖拽时中心点变化与瓦片请求方向一致

---

## 日志排障关键字

| 场景 | 关键字 |
|------|--------|
| 渲染 | `BMap::RequestRender start/end`、`context.renderDataList size` |
| 手势 | `OnTouchDown/OnTouchMove/OnTouchUp`（坐标是否连续） |
| 绘制 | `drawImage begin`、图层 `paint` 统计 |
| 数据 | 瓦片请求命中（cache/local/remote）日志 |
