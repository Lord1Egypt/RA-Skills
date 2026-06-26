---
name: baidu-map-ios-sdk
description: 百度地图 iOS SDK 与 BMKLocationKit 集成与开发规范。覆盖地图、定位、步骑行导航、检索、路线、标注与覆盖物；输出专业地图方案。可快捷使用百度地图 SDK 的能力与数据，构建功能丰富、交互性强的专业地图类应用。
compatibility: iOS, Xcode, CocoaPods
---

# 百度地图 iOS SDK

## 目标与边界

- **目标**：在 iOS 工程中正确集成百度地图/定位/步骑行导航，并给出符合隐私与坐标系规范的实现方案。
- **负责**：BaiduMapKit、BMKLocationKit、BaiduWalkNaviKit 的集成、配置、API 选用与示例；与技能内 reference 文档一致。
- **不负责**：驾车导航细节（百度地图驾车导航文档）、服务端逻辑、非百度 SDK、UI 视觉设计（仅遵循 [ui-standards.md](references/ui-standards.md) 的规范）。

## 使用时机

满足其一即启用本技能：

- 关键词：百度地图、BMKMapView、BMKLocationKit、步骑行导航、BaiduWalkNaviKit、标注、路线规划、CocoaPods 集成、BD09、定位鉴权
- 需求类型：地图展示、单次/连续/后台定位、步行或骑行实时导航、POI/标注/覆盖物、路线绘制、逆地理、轨迹动画、点聚合、隐私弹窗

**按需加载**：先根据需求在 [reference.md](references/reference.md) 中选定文档，再引用对应 references 内容；需求含糊时先向用户澄清再给方案。

## 集成与编码顺序

- **未集成百度地图 SDK 时**：先配置并执行 CocoaPods（编写/补全 Podfile → 执行 `pod install` → 使用生成的 `.xcworkspace` 打开），**在能正确导入 SDK 头文件之后**再编写调用地图/定位/检索等的代码。这样既避免使用 `#if __has_include(...)` 做条件编译，也能以实际 SDK 头文件为准写代码，减少接口不一致或编译错误。
- **本地已集成 SDK 时**：直接按需导入头文件并写代码，**以当前工程内的 SDK 版本、头文件及接口为准**；类名、方法、参数与本地头文件一致，不写不存在的 API。若编译报错提示符号不存在，提示开发者核对或更新 Pod 版本后再重试。

## Agent 执行要求

1. **AK 与 Bundle 主动提示**  
   在编写或集成使用地图/定位 SDK 的代码时，**主动提示开发者**：
   - 在 [百度 LBS 控制台](https://lbsyun.baidu.com/) 申请 **iOS 应用 AK**，且应用的 **Bundle Identifier** 必须与工程中 `PRODUCT_BUNDLE_IDENTIFIER` 一致；
   - 在代码或配置中预留/替换 AK 的位置（如 `AppDelegate` 中的 key、或说明需在控制台配置），并注明「将 `YOUR_AK` 替换为实际 AK」。
   - 若工程尚未配置 Bundle ID，提醒开发者设置并与控制台申请时填写的包名一致。

2. **代码写完自动执行编译修复，编译无误后停止**  
   完成与百度地图/定位相关的代码修改后，**必须**按以下流程执行，**不得在编译未通过时结束**：
   - **自动执行编译**：使用 `xcodebuild -workspace xxx.xcworkspace -scheme xxx -destination 'generic/platform=iOS' build`（或等价命令；CocoaPods 工程用 workspace，纯工程用 project）。
   - **若编译报错**：根据报错信息**立即修复**（类名、方法签名、头文件、ARC、协议声明等），修复后**再次执行编译**。
   - **循环**：重复「编译 → 若有错误则修复 → 再编译」，直至**编译通过、无错误**。
   - **编译无误后停止**：仅当 build 成功（BUILD SUCCEEDED）后，才结束本轮代码修改与修复，不再继续做与编译无关的额外修改。

3. **配置 Launch Screen 避免 App 非全屏**  
   集成地图或涉及全屏展示时，**必须**确保工程已配置 Launch Screen，避免运行后出现黑边、非全屏。具体见 [project-config.md](references/project-config.md)「窗口初始化/Launch Screen」：
   - 工程内存在 **LaunchScreen.storyboard**（或等效 Launch 资源），并加入 target 的 Resources；
   - Info.plist 中配置 **UILaunchStoryboardName** 为 `LaunchScreen`；
   - 若缺失，主动创建或补充说明，并提醒开发者添加该配置。

## 必须遵守的规则

1. **隐私与配置**
   - 首次使用前必须弹窗让用户阅读并同意隐私政策，再调用对应接口。
   - **地图**：`[BMKMapManager setAgreePrivacy:YES]`（**类方法**，勿用 `sharedInstance`；未同意时检索可返回 nil）。
   - **定位**：通过 **BMKLocationAuth** 的 **setAgreePrivacy** 在用户同意后再初始化 BMKLocationManager 等；详见 [location.md](references/location.md)。
   - Info.plist 必配 **CFBundleDisplayName**；使用定位时配 NSLocationWhenInUseUsageDescription 等。详见 [project-config.md](references/project-config.md)。
   - **AK 与 Bundle**：编写集成代码时主动提示开发者提供/配置 AK，且 Bundle Identifier 与百度控制台申请一致（见上文「Agent 执行要求」）。
   - **Launch Screen**：必须配置 LaunchScreen.storyboard 与 Info.plist 的 UILaunchStoryboardName，避免运行后 App 非全屏、黑边；见 [project-config.md](references/project-config.md)。

2. **坐标系**
   - 地图 SDK 全局 **BD09**；定位 SDK 默认 **GCJ02**。与地图混用时须统一为 BD09：将定位 **coordinateType** 设为 **BMKLocationCoordinateTypeBMK09LL**，或使用 [utils.md](references/utils.md) 的 BMKCoordTrans 转换。

3. **标注与几何（必须遵守）**
   - **点标注优先使用 Marker，不得使用 Annotation/PinAnnotation**：点标注**必须优先**使用 **BMKIconMarker/BMKTextMarker**（addOverlay 体系），**禁止**使用 BMKPointAnnotation、BMKAnnotationView、BMKPinAnnotationView（addAnnotation 体系）除非以下例外：点聚合（BMKClusterManager 必须用 BMKPointAnnotation）、固定屏选点（isLockedToScreen）等仅 addAnnotation 能实现的场景。起终点、小车、普通图钉等一律用 Marker。详见 [overlays.md](references/overlays.md)、[annotations.md](references/annotations.md)。
   - 距离、视野、方位等用 [utils.md](references/utils.md) 的 BMKGeometry 等，勿手写。
   - **路线与起终点须优先使用纹理**：绘制**路线**时优先使用 **BMKPolylineView.textureImage**（图片宽高须为 2 的 n 次幂）或路况场景使用 **BMKMultiTexturePolylineView** + [assets](references/assets.md) 路况纹理；**起终点**的 BMKIconMarker.icon 须优先使用 [assets](references/assets.md) 的 **icon_start、icon_end**；仅当无可用纹理时再使用 strokeColor/纯色或自绘。见 [overlays.md](references/overlays.md)「路线与起终点：纹理优先」。
   - **路线小车纹理**：路线上的小车图标**必须优先使用**本技能 [assets](references/assets.md)（`assets/images/`）提供的纹理图（如 icon_car、car_triangle、track_car）；仅当无可用纹理时，才使用纯色或自绘图片。

4. **步骑行：按需求区分两种方案**
   - **路线规划（算路+画线）**：BMKRouteSearch（BaiduMapKit），walkingSearch/ridingSearch，得到路线后自绘折线。见 [route.md](references/route.md)。
   - **步骑行实时导航**：BaiduWalkNaviKit，Manager + 诱导、TTS、偏航纠偏、多实例/无UI。见 [navi.md](references/navi.md)。
   - 二者是**不同服务**：仅需画线用 route；需实时导航用 navi。给出方案前先按开发者需求选对文档。

5. **版本与 API 以本地为准**（与上文「集成与编码顺序」一致）
   - 已集成 SDK：**以工程内 SDK 版本与头文件为准**，类名、方法、参数与头文件一致；不写 `#if __has_include`，直接导入头文件后写代码。
   - 若某类、方法或属性在用户工程中**不存在**（编译报错或头文件无此符号），**提示用户将对应 Pod 更新到最新版本**后再重试，勿强行按文档写不存在的 API。

6. **Logo 不可遮挡与路线视野适配（必须考虑）**
   - **Logo 不能被遮挡**：百度地图 Logo 不可移除、不允许被 UI 遮挡。有浮动栏/底部栏时**必须**使用 `setMapPadding` 预留边界（如顶部预留检索面板、底部预留 barH+4），使 Logo 落在可见内容区内。详见 [ui-standards.md](references/ui-standards.md)「地图 Logo、指南针与 mapPadding」。
   - **路线适配视野必须做**：有路线绘制时**必须**调用 `fitVisibleMapRect:edgePadding:withAnimated:` 做视野适配，edgePadding 按 [ui-standards.md](references/ui-standards.md)「路线视野适配」预留（顶部检索面板+50+marker、底部底部栏+20+marker、左右 50+marker 等），避免路线或起终点被裁切或被 UI 遮挡。mapPadding 与 fitVisibleMapRect 的 edgePadding 分开使用，勿混用。

## 输出规范（可评估）

给出方案时需满足：

- **可落地**：含具体类名、方法、调用顺序与必要配置（如 Info.plist、隐私调用时机、Launch Screen）。
- **可验证**：隐私与坐标系处理明确；若涉及定位鉴权失败，方案中可指向 [location.md](references/location.md) 的「鉴权失败排查」。
- **可组合**：按 [reference.md](references/reference.md) 选文档与常见组合；步骑行选型见规则 4。
- **AK/Bundle 提示**：涉及地图/定位初始化时，明确提示开发者配置 AK 与 Bundle Identifier。
- **编写后编译直至通过**：完成代码编写后，自动执行 xcodebuild 编译；若有报错则根据错误修复并重新编译，循环直至编译无误，再停止。
- **全屏与 Launch Screen**：涉及地图全屏或窗口大小时，确认或说明已配置 LaunchScreen.storyboard 与 UILaunchStoryboardName，避免运行后非全屏、黑边。
- **Logo 不遮挡**：涉及地图且有浮动栏/底部栏时，方案中**必须**包含 setMapPadding，并说明底部预留尽量小（如 barH+4），确保 Logo 不被遮挡。
- **路线视野适配**：涉及路线绘制时，方案中**必须**包含 fitVisibleMapRect 的 edgePadding 设置，按 ui-standards 预留顶底左右，确保路线与起终点在可视区内且不被 UI 遮挡。
- **点标注用 Marker**：涉及地图点标注（起终点、小车、图钉等）时，**必须**使用 BMKIconMarker/BMKTextMarker（addOverlay），不得使用 BMKPointAnnotation/BMKPinAnnotationView，除非点聚合、固定屏选点等例外场景。
- **路线与起终点纹理优先**：涉及路线折线或起终点 Marker 时，**必须**优先使用纹理（路线：BMKPolylineView.textureImage 或 BMKMultiTexturePolylineView；起终点：BMKIconMarker.icon 使用 [assets](references/assets.md) 的 icon_start/icon_end），仅无可用纹理时再写 strokeColor 或自绘；见 [overlays.md](references/overlays.md)「路线与起终点：纹理优先」。

方案结构：需求 → 对应文档 → 配置与依赖（含 AK/Bundle、Launch Screen）→ 关键 API → 示例片段 → 注意事项（含 Logo/路线视野、Marker 优先）。

## 参考索引

- 选文档与边界：[reference.md](references/reference.md)
- 类速查：[class-index.md](references/class-index.md)
- 定位/鉴权：[location.md](references/location.md) 
- 步骑行导航：[navi.md](references/navi.md) 
- 资源：[assets.md](references/assets.md)
