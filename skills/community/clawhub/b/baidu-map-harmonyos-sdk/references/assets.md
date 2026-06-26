# 图片资源

**边界**：技能内 `assets/images/` 图片及用途，**必须**需要将需要使用的图像资源拷贝到项目模块（module）资源文件目录（resources）下的rawfile文件夹中，如果无满足要求应用场景的图像资源，则通过生成svg图像资源形式提供使用。

| 图片 | 用途 |
|------|------|
| icon_car | 小车 marker |
| car_triangle | 带方向小车（车头朝上） |
| track_car | 带方向小车（车头朝右），**轨迹动画推荐** |
| icon_start | （位置点）起点标注 |
| icon_end | （位置点）终点标注 |
| icon_via | （位置点）途经点 |
| traffic_texture_* | （线）路况纹理，蚯蚓线纹理 |
| bg_* |（背景图）气泡、信息框背景图，**名称包含相对点的Located** （lb代表右侧上；lt代表右侧下），如果未能识别相对Marker或者Label覆盖物的的Located（方向），则优先使用bg_middle.png|
｜transparent.png｜（位置点）占位图标**透明图**可配合气泡、信息框实现无点覆盖物图标的效果｜

## 背景图 .9 拉伸参数指导

下表给出常用气泡背景图的推荐 `.9` 拉伸参数，便于在 `setBackground(image, { scaleX, scaleY, fillArea })` 中直接使用（可根据实际视觉效果微调）：

| name | scaleX | scaleY | fillArea | 说明 |
|------|--------|--------|----------|------|
| bg_middle.png | [50, 95] | [25, 50] | [50, 95, 25, 50] | 中间气泡，适合不关心相对 Marker 方向时的通用信息框 |
| bg_lb.png | [70, 220] | [35, 80] | [70, 220, 35, 80] | 左下带三角的对话气泡，三角在左下，拉伸区域避开三角和边框阴影。设置方位锚点为`SysEnum.Located.RIGHT_TOP`。 |
| bg_lt.png | [70, 220] | [30, 75] | [70, 220, 30, 75] | 左上带三角的对话气泡，三角在左上，拉伸区域避开三角和边框阴影。设置方位锚点为`SysEnum.Located.RIGHT_BOTTOM`。 |

