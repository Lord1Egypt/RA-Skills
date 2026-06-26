# 百度地图鸿蒙SDK开发指南

## 注册和获取密钥

### 什么是密钥

开发者在使用SDK之前需要获取百度地图移动版开发密钥（AK），该AK与您的百度账户相关联。地图初始化时需要使用AK，这是访问百度地图服务的必要前提，**请妥善保存您的AK，避免AK丢失和AK泄露。**

**在哪里可以查看我已申请的AK？**

点击控制台-应用管理-[我的应用](https://lbsyun.baidu.com/apiconsole/app)可查看您所申请的全部AK信息。

**如果我的AK被泄露会有什么后果？**

AK泄露会导致您的账号服务额度被盗用，导致服务消耗量增大，可能会消耗账户充值金额，或被他人用于从事不法活动，建议您谨慎保管您账号所有AK应用信息。

**如果我的AK被泄露应该怎么办？**

若AK已被泄露，建议您立即在控制台-应用管理-[我的应用](https://lbsyun.baidu.com/apiconsole/app)删除该项AK，重新更换AK进行服务调用

### 获取开发密钥(AK)

请在控制台-[我的应用](https://lbsyun.baidu.com/apiconsole/app)申请SDK开发密钥

申请步骤大致可分为如下四个步骤：

1. 若您未登录百度账号，请登录您的百度账号，如下图：

（若您没有百度账号，点击右下角根据提示注册并登录）

2. 登录后将进入官网控制台，如下图：

3. 点击【我的应用】、【创建应用】开始申请开发密钥，如下图：

4. 填写应用名称，选择【应用类型】选择“鸿蒙 SDK”、选择【启用服务】，并填写【AppID】（获取方式参考下方介绍）。如下图：

注意：「启动服务」中的各项服务须勾选后才能正常使用，取消勾选会导致AK没有使用对应服务的权限，若您没有特殊要求，建议保持默认勾选。例如，如果您在申请时没有勾选“国内天气查询”，则申请到的AK访问过那天起查询时会返回无权限。

**申请AK时没有选择某项服务，我该如何重新勾选**

请点击控制台-应用管理-我的应用，找到对应AK点击设置，重新勾选所需服务

5. 完成以上内容之后点击提交会为您生成该应用的AK，到这您就可以使用AK来开始开发工作了。

### 获取AppIdentifier（官网注册所用的AppID）

```typescript
  public getBundleAppIdentifier() {
       // 根据给定的bundle名称获取BundleInfo。 
       // 使用此方法需要申请 ohos.permission.GET_BUNDLE_INFO权限。 
       let bundleFlags = bundleManager.BundleFlag.GET_BUNDLE_INFO_WITH_SIGNATURE_INFO;
       try {
          return bundleManager.getBundleInfoForSelf(bundleFlags).then((data) => {
          //获取appIdentifier 
             appIdentifier = data.signatureInfo.appIdentifier;
             console.info("getBundleAppIdentifier successfully. Data: " + appIdentifier );
          }).catch(error => {
             console.error("getBundleAppIdentifier failed. Cause: " + error.message);
          });
       } catch (error) {
           console.error("getBundleAppIdentifier failed:" + error.message);
       }
}
```

获取正确的AppIdentifier，以确保在应用的调试和上线阶段能够顺利使用百度地图SDK:

appIdentifier指应用的唯一标识，由云端统一分配。该ID在应用全生命周期中不会发生变化，包括版本升级、证书变更、开发者公私钥变更、应用转移等。因此，开发者应使用云端分配的appIdentifier申请鸿蒙版百度地图SDK（以下简称：地图SDK）。大致流程如下：

1. 在AppGalleryConnect(AGC)上新建应用, 获取AppIdentifier, 获取地图SDK密钥:

c. 以上步骤完成后，即可使用AGC中相应应用的APP ID(AGC应用信息界面中的Key: "APP ID"对应的值即为AppIdentifier)申请地图SDK密钥

AGC云端应用的包名需要与本地工程一致, 可查看本地app.json5文件中配置的bundleName确认包名

2. 配置证书和profile，将云端信息绑定至本地工程

b. 使用生成的证书请求文件获取证书和profile:[https://developer.huawei.com/consumer/cn/doc/app/agc-help-releaseharmony-0000001933963166](https://developer.huawei.com/consumer/cn/doc/app/agc-help-releaseharmony-0000001933963166)

无论证书还是profile，调试和发布类型对应的AppIdentifier是一致的

c. 配置到本地工程:

i: 打开Project Strucure

ii: 点击Sining Configs, 取消勾选自动签名, 并配置密钥以及证书文件等信息。

iii: 获取本地AppIdentifier，确认是否与云端一致。


## 工程配置

### 1. 权限配置

在module.json5文件中配置HarmonyOS轻量地图SDK所需的相关权限，确保SDK可以正常使用。配置如下：

```json
"requestPermissions": [
      {
        "name": "ohos.permission.INTERNET"
      },
      {
        "name": "ohos.permission.GET_BUNDLE_INFO"
      }
    ]
```

### 2. 添加百度地图SDK依赖

可通过[OpenHarmony三方库中心仓](https://repo.huaweicloud.com/ohpm/cn/npm/@bdmap)查看百度地图提供的三方库列表以及版本更新情况。

安装过程可采用下面两种方式中的任意一种。

一种是通过命令安装指定版本的三方库，`<package_name>`换成安装的库名，`<version>`换成对应的版本

```bash
ohpm install @bdmap/<package_name>@<version>
```

另一种是通过配置文件，触发IDE 的 Sync Now拉取三方库。

在工程的oh-package.json5文件中添加依赖。配置如下：

```json
{
  "license": "Apache License 2.0",
  "devDependencies": {},
  "name": "entry",
  "description": "example description",
  "version": "1.0.1",
  "dependencies": {
    "@bdmap/base": "version",
    "@bdmap/search": "version",
    "@bdmap/map": "version"
  }
}
```

### 3. 获取HarmonyOS应用的appIdentifier

注意：请在真机运行下获取appId。使用云真机获取到的appId信息不全，会导致SDK鉴权失败，地图功能无法正常使用。

在Ability中调用如下代码来获取appIdentifier：

```typescript
  public getBundleAppIdentifier() {
      // 根据给定的bundle名称获取BundleInfo。 
      // 使用此方法需要申请 ohos.permission.GET_BUNDLE_INFO权限。 
      let bundleFlags = bundleManager.BundleFlag.GET_BUNDLE_INFO_WITH_SIGNATURE_INFO;
      try {
        return bundleManager.getBundleInfoForSelf(bundleFlags).then((data) => {
        //获取appIdentifier 
          appIdentifier = data.signatureInfo.appIdentifier;
          console.info("getBundleAppIdentifier successfully. Data: " + appIdentifier );
        }).catch(error => {
          console.error("getBundleAppIdentifier failed. Cause: " + error.message);
        });
      } catch (error) {
        console.error("getBundleAppIdentifier failed:" + error.message);
      }
    }
```

### 4. 申请AK

申请所需参数：appIdentifier。联系开放平台。

### 5. SDK集成说明

百度地图HarmonyOS SDK提供两种集成方式：分体包和组合包。两种方式互斥，开发者需根据业务需求选择其一。

#### 5.1 集成方式

**方式一：分体包集成**

适用于基础地图功能开发，支持按需引入模块。

*   @bdmap/base: 基础库，提供通用API和工具类
*   @bdmap/map: 地图可视化模块，依赖base
*   @bdmap/search: 检索服务模块，依赖base
*   @bdmap/util:工具库模块，依赖base

集成示例：

```json
{
  "dependencies": {
    "@bdmap/base": "2.0.3",
    "@bdmap/map": "2.0.3",
    "@bdmap/search": "2.0.3",
    "@bdmap/util": "2.0.3"
  }
}
```

**方式二：组合包集成**

适用于驾车导航/步骑行导航功能开发，集成所有基础模块及导航专用接口。

*   @bdmap/navi_map: 百度驾车导航SDK，集成base、map、search、util等所有基础功能
*   @bdmap/map_walkride_search: 步骑行导航SDK，集成base、map、search、util等所有基础功能

集成示例：

```json
{
  "dependencies": {
    "@bdmap/navi_map": "1.0.1"
  }
}
```

或

```json
{
  "dependencies": {
    "@bdmap/map_walkride_search": "2.0.3"
  }
}
```

#### 5.2 重要约束

1.  互斥性: 分体包与组合包不可同时使用
2.  版本一致性: 同一项目内所有@bdmap/包版本必须保持一致
3.  依赖管理: 组合包已内置所有基础模块，无需额外引入分体包

#### 5.3 选择建议

*   基础地图应用: 使用分体包，按需引入模块
*   导航应用: 使用组合包，获得完整导航能力

---

# 功能分类

本文档按照功能模块进行分类组织，便于快速查找相关技能指导。

## 快速索引

- **地图展示与交互（`@bdmap/map`）**：MapComponent、MapController、onReady、MapOptions、MapStatus、MapEvent、手势、控件、事件、室内图、离线地图、销毁地图、英文地图、粒子效果、定位图层、指南针/方向图层
  - docs 入口：`api/modules/map.md`
- **覆盖物绘制（`@bdmap/map`）**：Marker、Polyline、Polygon、Circle、Label、PopView、InfoWindow、ClusterGroup（点聚合）、Track/TrackAnimation、HeatMapBuilder、HexagonMapBuilder、UrlTileProvider/ImageTileLayer、MultiPoint、Prism、Building、Bd_3DModel
  - docs 入口：`api/modules/map.md`
- **检索能力（`@bdmap/search`）**：PoiSearch、GeoCoder、AoiSearch、SuggestionSearch、BusLineSearch、WeatherSearch、DistrictSearch、BuildingSearch、RecommendStop
  - docs 入口：`api/modules/search.md`
- **路线规划（`@bdmap/search` + `walkridecommon` 或组合包）**：RoutePlanSearch、drivingSearch、walkingSearch、bikingSearch、transitSearch、masstransitSearch
  - docs 入口：`api/modules/search.md`、`api/modules/walkridecommon.md`
- **工具类能力与其他（`@bdmap/util` / `@bdmap/base` / `@bdmap/map`）**：DistanceUtil、AreaUtil、SpatialRelationUtil、NativeMethods（坐标转换）、FavoriteManager、ShareUrlSearch
  - docs 入口：`api/modules/util.md`、`api/modules/base.md`

## 1. 地图展示与交互（模块：map）

> 模块：`@bdmap/map`　docs：`api/modules/map.md`　常用检索词：MapComponent / MapController / MapOptions / MapStatus / MapEvent / gestures / indoorMap / LocalMapManager / onWillDisappear / MapLanguage

### 显示地图

百度地图HarmonyOS NEXT版地图SDK为开发者提供了便捷的地图渲染SDK。

#### 创建地图

只需要按照如下操作，即可快速进行百度地图展示：

1. 第一步 在绘制地图前初始化SDK，如下：

```typescript
// SDK初始化需要传入UIAbility上下文，建议在MainAbility中调用初始化函数。
Initializer.getInstance().initialize("Your API_KEY", this.context);
```

2. 第二步 创建MapComponent

```typescript
// 设置地图控件参数
  mapOpt: MapOptions = new MapOptions({ 
      // 配置地图状态，如地图缩放等级、显示中心点、旋转角等
      mapStatus: new MapStatus(),
      // 默认基础地图，可通过改变satelliteMap的值加载不同的底图
      shows:{satelliteMap:SysEnum.ESatelliteLayerType.NONE}
  });

// 地图初始化的回调
this.callback = async (err, mapController:MapController) => {
  if (!err) {
    // 获取地图的控制器类，用来操作地图
    this.mapController= mapController;
  }
};

MapComponent({ onReady: this.callback, mapOptions: this.mapOpt }).width("100%").height("100%")
```

#### 地图类型切换

通过`mapController.setMapType`方法切换不同的地图类型，目前提供三种地图类型：普通图，卫星图，空白地图

```typescript
this.mapController.setMapType(SysEnum.MapType.MAP_TYPE_NORMAL); // 普通图
this.mapController.setMapType(SysEnum.MapType.MAP_TYPE_SATELLITE); // 卫星图
this.mapController.setMapType(SysEnum.MapType.MAP_TYPE_NONE); // 空白地图
```

#### 地图POI显隐控制

可通过设置基础POI和室内图POI的显示隐藏。

```typescript
this.mapController.mapOptions.showMapPoi = true;
this.mapController.mapOptions.showMapIndoorPoi = true;
```

#### 地图楼块显隐控制

可通过设置楼块以及3D模型的显示隐藏。

```typescript
// 设置楼块是否有高度
this.mapController.setHouseHeightEnable(boolean);

// 设置是否显示3D模型
this.mapController.set3DModelEnable(boolean);
```

#### 交通流控制

可通过下面两种形式改变地图交通流显示状态：

一种是通过地图初始化设置MapOptions时设置trafficMap的参数来配置是否显示交通流；

一种是通过给MapOptions.showTrafficMap赋值形式改变。

示例代码如下：

```typescript
// 初始化配置形式
mapOpt: MapOptions = new MapOptions(shows:{trafficMap:true}});

// 显示交通流
this.mapController.mapOptions.showTrafficMap = true;

// 不显示交通流
this.mapController.mapOptions.showTrafficMap = false;
```

#### 百度城市热力图

百度城市热力图是百度基于强大的地理位置大数据，根据实时的人群分布密度和变化趋势，用热力图的形式展现给广大开发者。

百度城市热力图的使用方式和实时路况图类似，只需要简单的接口调用，即可在地图上展现样式丰富的热力图层。

注意：只有在地图层级大于等于11级时，可显示城市热力图。

```typescript
// 开启百度城市热力图
this.mapController.setBaiduHeatMapEnabled(true);

// 关闭百度城市热力图
this.mapController.setBaiduHeatMapEnabled(false);
```

普通地图叠加热力图显示效果如下

### 个性化地图

为适配不同的应用场景和APP风格，支持开发者自定义配置地图样式，自由控制底图50多种元素（包含陆地、水系、绿地、人造区域、建筑物、道路、铁路、地铁，POI等）的颜色、透明度、显隐等呈现效果。

注意：个性化地图需要搭配[个性化编辑器](https://lbsyun.baidu.com/apiconsole/custommap)使用，编辑好地图样式后再导入到自己的应用程序中。

#### 使用步骤

[选择模版/编辑个性化地图](https://lbsyun.baidu.com/apiconsole/custommap)——传入.sty文件路径/样式ID——开始使用个性化地图

1. 选择模板 or 编辑个性化地图

开发者可选择模版或者新建并配置个性化地图，打造独具风格与特色的地图。

2. 发布样式，传入.sty文件路径/样式ID

3. 使用个性化地图

**方式一：配置.sty样式ID**

```typescript
class CustomMapStyleCallBackImpl implements CustomMapStyleCallBack {

   /*
       * @return 返回true:表示这部分逻辑由开发者处理,SDK不做任何处理,即新的样式更新需要开发者自行实现；
       *         返回false:默认走SDK内部处理逻辑
   */
    onPreLoadLastCustomMapStyle(path: string | null) {
        console.log(`CustomMapStyle-本地缓存: ${path ?? '无'}`);
        return false;
    }
    onCustomMapStyleLoadSuccess(hasUpdate: boolean, path: string | null) {
        console.log(`CustomMapStyle-加载成功, 是否更新: ${hasUpdate}, 路径: ${path}`);
        return false;
    }
    onCustomMapStyleLoadFailed(status: number, message: string, path: string | null) {
        console.error(`CustomMapStyle-加载失败, status: ${status}, message: ${message}, path: ${path}`);
        return true;
    }
}

const styleCallBack: CustomMapStyleCallBack = new CustomMapStyleCallBackImpl();

this.mapController?.setCustomStyleById('xxxxxxxxxxxxxxxxx', styleCallBack);
```

**方式二：加载样式文件**

在项目资源目录rawfile中拷贝map.sty文件，可以重命名，比如map_gray.sty。然后通过initCustomStyle方法加载样式，通过setCustomStyleEnable方法设置是否启用此样式。

```typescript
// 加载个性化样式文件
 this.mapController.initCustomStyle('map_gray.sty', () => {
      // 设置是否启用此样式
      this.mapController?.setCustomStyleEnable(true);
 });
```

### 室内图控制

室内图支持的公众建筑包含购物商场、机场和火车站等交通枢纽，医院等。

#### 设置室内图显示状态

室内图默认不显示，如果需要显示，可通过下面两种方式设置：

一种是：地图初始化时设置indoorMap是否显示；

一种是：通过MapOptions的showBaseIndoorMap设置是否显示。

```typescript
// 地图初始化设置
mapOpt = new MapOptions({ shows:{indoorMap:true}});

// 地图实例化后设置
this.mapController.mapOptions.showBaseIndoorMap = true;
```

#### 设置监听事件来监听进入和移出室内图

通过设置地图的MapEvent.INDOORSTATUSCHANGE事件，监听地图室内图状态，判断是否进入室内图或者移出室内图。

```typescript
this.mapController.addEventListener(MapEvent.INDOORSTATUSCHANGE, (status) => {
    if (status) {
        // 进入室内图
    } else {
        // 移除室内图
    }
});
```

#### 实现楼层间地图切换,展示不同楼层的室内图

首先是通过地图实例的getIndoorInfo(uid?:string)方法获取室内楼层数据，uid参数可选，若无，则获取当前地图范围内显示的室内图楼层数据。

```typescript
let data = this.mapController.getIndoorInfo(uid) as null | IndoorFloorBundles;
if (data && data.uid) {
    data.floorlist.map((floorName: string) => {
        // 楼层名称
    });
}
```

然后，通过switchIndoorFloor(floor:string,uid:string)切换显示室内图楼层

```typescript
this.mapController.switchIndoorFloor(floorName, uid);
```

### 离线地图

#### 简介

LocalMapManager提供了完整的离线地图下载、管理和状态监控功能。通过这个类，你可以轻松实现城市离线地图的下载、暂停、恢复、删除等操作。

#### 快速开始

1. 基础初始化

```typescript
import { LocalMapManager,LocalMapListener,LocalMapConstants } from '@bdmap/map';

// 1. 获取单例实例
const localMapManager = LocalMapManager.getInstance();

// 2. 在地图初始化完成后初始化离线地图模块
// 注意：必须在MapController准备好后调用
const success = localMapManager.init(mapController);
if (success) {
  console.log('离线地图模块初始化成功');
}
```

2. 设置事件监听

```typescript
// 创建事件监听器
const mapListener: LocalMapListener = {
  onGetLocalMapState: (type: number, param: number) => {
    console.log(`离线地图事件: type=${type}, param=${param}`);
    switch (type) {
      case LocalMapConstants.MESSAGE_START_DOWNLOAD:
        console.log('开始下载');
        break;
      case LocalMapConstants.MESSAGE_DOWNLOAD_PROGRESS:
        // 解析下载进度参数
        const cityId = param >> 8;      // 右移8位获取城市ID
        const progress = param & 0xFF;  // 取低8位获取进度
        console.log(`城市 ${cityId} 下载进度: ${progress}%`);
        break;
      case LocalMapConstants.MESSAGE_DOWNLOAD_FINISHED:
        console.log('下载完成');
        // 下载完成后建议导入地图
        localMapManager.importMap(true, false);
        break;
      case LocalMapConstants.MESSAGE_NETWORK_ERROR:
        console.log('网络错误，下载中断');
        break;
    }
  }
};

// 注册监听器
localMapManager.registerListener(mapListener);
```

#### 城市数据获取

**获取热门城市列表**

```typescript
// 获取热门城市（适合在首页展示）
async function loadHotCities() {
  try {
    const cities = await localMapManager.getHotCities();
    if (cities && cities.length > 0) {
      console.log(`获取到 ${cities.length} 个热门城市`);
      cities.forEach(city => {
        console.log(`${city.name} - 大小: ${formatSize(city.mapsize + city.searchsize)}`);
      });
    }
  } catch (error) {
    console.error('获取热门城市失败:', error);
  }
}

// 辅助函数：格式化文件大小
function formatSize(size: number): string {
  if (size < 1024 * 1024) {
    return `${Math.floor(size / 1024)}K`;
  } else if (size < 1024 * 1024 * 1024) {
    return `${(size / (1024 * 1024.0)).toFixed(1)}M`;
  } else {
    return `${(size / (1024 * 1024 * 1024.0)).toFixed(1)}G`;
  }
}
```

**搜索城市**

```typescript
// 根据关键词搜索城市
function searchCities(keyword: string) {
  if (!keyword.trim()) {
    return [];
  }
  const results = localMapManager.getCitiesByName(keyword);
  if (results && results.length > 0) {
    console.log(`搜索"${keyword}"找到 ${results.length} 个城市`);
    return results;
  }
  console.log(`未找到包含"${keyword}"的城市`);
  return [];
}
```

**获取用户下载记录**

```typescript
// 获取用户所有下载记录
async function getUserDownloadList() {
  try {
    const resources = await localMapManager.getUserResources();
    if (resources && resources.length > 0) {
      // 分类整理下载记录
      const downloadingCities = resources.filter(city => 
        LocalMapResourceUtils.isDownloading(city) || 
        LocalMapResourceUtils.isWaiting(city) ||
        LocalMapResourceUtils.isStoped(city)
      );
      const downloadedCities = resources.filter(city => 
        LocalMapResourceUtils.isFinished(city)
      );
      console.log(`下载中: ${downloadingCities.length} 个城市`);
      console.log(`已完成: ${downloadedCities.length} 个城市`);
      return { downloadingCities, downloadedCities };
    }
  } catch (error) {
    console.error('获取下载记录失败:', error);
  }
  return { downloadingCities: [], downloadedCities: [] };
}
```

### 下载管理

**开始下载城市**

```typescript
// 下载单个城市（带重复检查）
function downloadCity(
  city: LocalMapResource,
  downloadingList: LocalMapResource[],
  downloadedList: LocalMapResource[]
) {
  // 防重复下载检查
  const isAlreadyDownloaded = downloadedList.some(item => item.id === city.id);
  const isDownloading = downloadingList.some(item => item.id === city.id);
  if (isAlreadyDownloaded) {
    console.log(`${city.name} 已经下载完成，无需重复下载`);
    return false;
  }
  if (isDownloading) {
    console.log(`${city.name} 正在下载中，请勿重复操作`);
    return false;
  }
  // 开始下载
  const success = localMapManager.start(city.id);
  if (success) {
    console.log(`开始下载 ${city.name}`);
  } else {
    console.log(`下载失败 ${city.name}`);
  }
  return success;
}
```

**暂停和恢复下载**

```typescript
// 暂停指定城市下载
function pauseCity(cityId: number) {
  const success = localMapManager.pause(cityId);
  if (success) {
    console.log(`已暂停城市 ${cityId} 的下载`);
  }
  return success;
}

// 恢复指定城市下载
function resumeCity(cityId: number) {
  const success = localMapManager.resume(cityId);
  if (success) {
    console.log(`已恢复城市 ${cityId} 的下载`);
  }
  return success;
}

// 批量暂停所有下载
function pauseAllDownloads() {
  const success = localMapManager.pauseAll(0); // 0表示批量暂停
  if (success) {
    console.log('已暂停所有下载任务');
  }
  return success;
}

// 批量恢复所有下载
function resumeAllDownloads() {
  const success = localMapManager.resumeAll(0); // 0表示下载
  if (success) {
    console.log('已恢复所有下载任务');
  }
  return success;
}
```

**删除下载任务**

```typescript
// 删除指定城市
function deleteCity(cityId: number) {
  const success = localMapManager.delete(cityId);
  if (success) {
    console.log(`已删除城市 ${cityId}`);
  }
  return success;
}

// 删除所有下载任务
function deleteAllCities() {
  const success = localMapManager.deleteAll();
  if (success) {
    console.log('已删除所有城市离线地图');
  }
  return success;
}
```

#### 状态管理

**判断城市状态**

```typescript
import { LocalMapResourceUtils } from '@bdmap/map';

function getCityStatus(city: LocalMapResource): string {
  if (LocalMapResourceUtils.isWaiting(city)) {
    return '等待下载';
  } else if (LocalMapResourceUtils.isDownloading(city)) {
    return `下载中 ${city.downloadProgress}%`;
  } else if (LocalMapResourceUtils.isStoped(city)) {
    return '已暂停';
  } else if (LocalMapResourceUtils.isFinished(city)) {
    return '下载完成';
  } else if (LocalMapResourceUtils.isNeedUpdate(city)) {
    return '需要更新';
  } else {
    return '未下载';
  }
}

// 检查是否可以执行特定操作
function canResumeDownload(city: LocalMapResource): boolean {
  return LocalMapResourceUtils.isCanResume(city);
}

function needsUpdate(city: LocalMapResource): boolean {
  return LocalMapResourceUtils.isNeedUpdate(city);
}
```

**实时状态刷新**

```typescript
// 推荐的状态刷新策略
class OfflineMapManager {
  private refreshTimer: number = -1;

  // 启动定时刷新（仅在有下载任务时）
  startAutoRefresh(downloadingCities: LocalMapResource[]) {
    // ... (代码已截断，完整内容请参考原始文档)
  }
}
```

### 英文地图

#### 快速开始

1. 导入必要的模块

在使用英文地图功能前，需要导入以下模块：

```typescript
import{ MapComponent, MapController, MapLanguage, MapOptions, MapStatus }from"@bdmap/map";
```

**关键类型说明：**

*   MapController: 地图控制器，用于控制地图的各种操作
*   MapLanguage: 地图语言枚举，包含CHINESE和ENGLISH两个选项
*   MapComponent: 地图组件，用于在 UI 中显示地图

2. 设置英文地图

通过MapController的setMapLanguage()方法设置地图语言：

```typescript
// 设置为英文地图
this.mapController?.setMapLanguage(MapLanguage.ENGLISH);

// 设置为中文地图
this.mapController?.setMapLanguage(MapLanguage.CHINESE);
```

### API 说明

**MapLanguage 枚举**

```typescript
export enum MapLanguage {
CHINESE=0, // 中文
ENGLISH=1 // 英文
}
```

**MapController.setMapLanguage()**

**方法签名：**

`setMapLanguage(language: MapLanguage):void`

**参数说明：**

*   language: 要设置的地图语言，使用MapLanguage.ENGLISH或MapLanguage.CHINESE

**功能说明：**

设置地图显示语言会自动处理语言持久化存储

**注意事项：**

*   确保mapController不为null再调用此方法
*   语言设置会自动持久化，下次打开地图时会保持上次设置的语言

**MapController.getMapLanguage()**

**方法签名：**

`getMapLanguage():number`

**返回值：**

返回当前地图语言的枚举值（MapLanguage.CHINESE或MapLanguage.ENGLISH）

**使用示例：**

```typescript
const currentLanguage:number=this.mapController?.getMapLanguage();
if(currentLanguage === MapLanguage.ENGLISH){
console.log("当前是英文地图");
}else{
console.log("当前是中文地图");
}
```

### 粒子效果

鸿蒙地图SDK支持在地图上展示粒子效果，目前支持：雪花、雷雨、雾霾、沙尘、烟花、花瓣多种效果展示及自定义粒子效果。

#### 示例代码

```typescript
// 添加雪花粒子效果
this.mapController?.showParticleEffectByType(SysEnum.ParticleEffectType.Snow);

private async createBitmapDescriptor(res: Resource): Promise<image.PixelMap> {

    const context = getContext();

    const uint8 = await context.resourceManager.getMediaContent(res.id);

    const buffer = uint8.buffer.slice(uint8.byteOffset, uint8.byteOffset + uint8.byteLength);

    const imageSource = image.createImageSource(buffer);

    const decodingOptions: image.DecodingOptions = {

        editable: false,

        desiredPixelFormat: 3,

    };

    const pixelMap = await imageSource.createPixelMap(decodingOptions);

    imageSource.release();

    return pixelMap;

}

// 添加自定义粒子效果
const particleOptions = new ParticleOptions();
const position = new LatLng(39.914935, 112.403119);
particleOptions.setParticlePos(position);
const particleImgs: Array<image.PixelMap> = [];
const bullet = await this.createBitmapDescriptor($r("app.media.icon"));
const tail = await this.createBitmapDescriptor($r("app.media.icon"));
particleImgs.push(bullet, tail);
particleOptions.setParticleImgs(particleImgs);
await this.mapController?.customParticleEffectByType(
    SysEnum.ParticleEffectType.Fireworks,
    particleOptions
);

// 关闭粒子效果
this.mapController?.closeParticleEffectByType(SysEnum.ParticleEffectType.Snow);
```


### 销毁地图

#### 背景

在页面切换的时候，如果连续跳转的页面都使用了地图组件，对于地图组件的释放必须遵循"先销毁后创建"的栈式语义。

#### 路由框架分类与处理策略

1) 已知“栈式下发”的路由框架（系统Router 框架）

*   特性：生命周期严格按栈式下发，aboutToDisappear可靠早于对端出现。
*   建议：地图组件在收到aboutToDisappear时可安全自我销毁，开发者无需关注。

2) 已知支持“可打断动画”的路由框架（系统Navigation、HMRouter框架等）

*   特性：为支持打断/反转，aboutToAppear可能早于前一页的aboutToDisappear。
*   风险：若仅依赖aboutToDisappear，销毁会被动画延后，影响严格的栈式释放。
*   建议（必须执行）：在旧页面的onWillDisappear主动调用当前地图实例的onWillDisappear()。

##### 2.1 开发指导

**场景A （新建工程，Navigation）**

*   MapComponent 的 onReady 回调中获取 MapController。
*   页面 NavDestination 的 onWillDisappear 生命周期回调中，调用 mapController.onWillDisappear()。

```typescript
import { MapComponent, MapController} from "@bdmap/map"
import { AsyncCallback } from "@kit.BasicServicesKit";

@Builder
export function MapPageOneBuilder(name: string, param: Object) {
  MapPageOneComponent();
}

@Component
struct MapPageOneComponent {
  private stack: NavPathStack | null = null;
  @State eventStr: string = "";
  mapController: MapController | null = null
  private onReady: AsyncCallback<MapController> = async (err, mapCtrl) => {
    if (mapCtrl) {
      this.mapController = mapCtrl
    }
  }
  build() {
    NavDestination() {
      Column() {
        MapComponent({
          onReady: this.onReady
        })
          .height("70%")
        Button("pushPath", { stateEffect: true, type: ButtonType.Capsule })
          .width("80%")
          .height(40)
          .margin(20)
          .onClick(() => {
            if (this.stack) {
              this.stack.pushPath({ name: "MapPageOne" });
            }
          })
        Button("pop", { stateEffect: true, type: ButtonType.Capsule })
          .width("80%")
          .height(40)
          .margin(20)
          .onClick(() => {
            this.stack?.pop();
          })
      }
      .width("100%")
      .height("100%")
    }
    .title("pageOne")
    .onWillDisappear(() => {
      this.mapController?.onWillDisappear()
    })
    .onReady((ctx: NavDestinationContext) => {
      try {
        this.eventStr += "<onReady>";
        this.stack = ctx.pathStack;
      } catch (e) {
        console.error(`testTag onReady catch exception: ${JSON.stringify(e)}`);
      }
    })
  }
}
```

示例源码：

**场景B（既有工程，HMRouter）**

*   核心思路：维护“当前活跃地图”的全局列表。通过 HMRouter 注册全局生命周期监听，当收到 onWillDisappear 时，遍历全局列表并逐个触发控制器的销毁入口，随后清空列表。
*   全局状态：保存活跃的 MapController：

```typescript
// Global.ets（示例）
import { MapController } from "@bdmap/map_walkride_search";

export class GlobalState {
  public static context: Context;
  public static mapControllers: Array<MapController> = [];
  public static destroyMapControllers () {
    GlobalState.mapControllers.forEach((controller: MapController): void => controller?.onWillDisappear());
    GlobalState.mapControllers.length = 0;
  }
}

// MapComponentPage.ets（示例）
@Component
export struct MapComponentPage {
  build() {
    Stack({ alignContent: Alignment.TopStart }) {
      MapComponent({
        onReady: (err, mapController: MapController) => {
          if (mapController) {
            // 保存到全局列表
            GlobalState.mapControllers.push(mapController)
            }
        }
      }).width("100%").height("100%")
    }.width("100%").height("100%")
  }
}
```

HMRouter 注册全局生命周期监听

```typescript
// PageDurationLifecycle.ets（示例）
export class PageDurationLifecycle implements IHMLifecycle {
  onShown(ctx: HMLifecycleContext): void {
    const pageName = ctx.navContext?.pathInfo.name;
    console.log("PageDurationLifecycle",`Page ${pageName} onShown at ${new Date()}`);
  }
  onWillDisappear(ctx: HMLifecycleContext): void {
    const pageName = ctx.navContext?.pathInfo.name;
    console.log("PageDurationLifecycle",`Page ${pageName} onWillDisappear at ${new Date()}`);
    console.log(`PageDurationLifecycle::DestroyMapControllers GlobalState.mapControllers.length: ${GlobalState.mapControllers.length}`);
    // 收到回调触发销毁
    GlobalState.destroyMapControllers();
  }
  onHidden(ctx: HMLifecycleContext): void {
    const pageName = ctx.navContext?.pathInfo.name;
    console.log("PageDurationLifecycle",`Page ${pageName} onHidden at ${new Date()}`);
  }
}

// Index.ets（示例）
import { HMDefaultGlobalAnimator, HMNavigation, HMRouterMgr } from "@hadss/hmrouter";
import { AttributeUpdater } from "@kit.ArkUI";
import { PageDurationLifecycle } from "../common/PageDurationLifecycle";

@Entry
@Component
struct Index {
  modifier: MyNavModifier = new MyNavModifier();
  aboutToAppear(): void {
    HMRouterMgr.registerGlobalLifecycle({
      lifecycle: new PageDurationLifecycle(),
      lifecycleName: "PageDurationLifecycle",
      priority: 5
    });
  }
  build() {
    Column() {
      HMNavigation({
        navigationId: "mainNavigation",
        homePageUrl: "your_home_url",
        options: {
          standardAnimator: HMDefaultGlobalAnimator.STANDARD_ANIMATOR,
          dialogAnimator: HMDefaultGlobalAnimator.DIALOG_ANIMATOR,
          modifier: this.modifier
        }
      })
    }
    .width("100%")
    .height("100%")
  }
}
```

3) 其他第三方路由框架（时序特征不一）

说明：不同框架的转场实现与动画调度差异较大，生命周期回调先后可能与系统 Router/Navigation 不同。

建议（通用安全方案）：

*   在“页面将离场”的回调（如onWillDisappear或框架提供的等效钩子）调用onWillDisappear()，确保地图生命周期以栈式语义执行。
*   如框架支持"动画可打断/反转"，务必采用第2 类方案。

### 手势交互

HarmonyOS NEXT版地图SDK支持多种手势操作地图，包括拖动平移、双指缩放、双指旋转等，以及手势回调。

#### 手势控制

可通过地图初始化MapOptions的gestures控制是否允许手势交互；或者通过地图实例的MapOptions属性配置。

```typescript
// 初始化参数配置
mapOpt: MapOptions = new MapOptions({  
        gestures: {
            zoom: true,
            move: true,
            rotate: true,
            overlooking: true,
        }
    });

// 通过MapOptions属性配置
this.mapController.mapOptions.zoomGesturesEnabled = true; // 是否允许通过手势缩放地图
this.mapController.mapOptions.moveGesturesEnabled = false; // 是否允许通过手势移动地图
this.mapController.mapOptions.rotateGesturesEnabled = false; // 是否允许通过手势旋转地图
this.mapController.mapOptions.overlookingGesturesEnabled = false; // 是否允许通过手势俯仰地图
```

### 地图缩放中心点控制

可通过useMapCenterWhenPinch设置手势缩放中心点是否一直是地图显示区域的中心点位置。

```typescript
this.mapController.mapOptions.useMapCenterWhenPinch = true;
```

可通过MapOptions.zoomCenter设置手势缩放中心点是否是某一具体的地理位置。

```typescript
this.mapController.mapOptions.zoomCenter = new LatLng(39.412935, 115.433119);
```

### 控件交互

目前支持用户设置缩放控件、定位控件、比例尺控件的显示/隐藏以及显示位置。

```typescript
import { MapComponent, MapController, MapOptions, MapStatus, MapUIOperateModel} from "@bdmap/map";

mapController: MapController | null = null;
mapOpt: MapOptions = new MapOptions({
    mapStatus: new MapStatus({ zoom: 16 })
});
mapUIOperateModel: MapUIOperateModel = new MapUIOperateModel()

Button("显示", { type: ButtonType.Capsule, stateEffect: true }).onClick(() => {
        // 缩放控件
        this.mapUIOperateModel.getScaleView()
            .setShow(true)
        // 比例尺控件
        this.mapUIOperateModel.getZoom()
            .setShow(true)  // 是否显示
    }).borderRadius(8)
        .backgroundColor(0x317aff)
        .margin(5)

Button("隐藏", { type: ButtonType.Capsule, stateEffect: true }).onClick(() => {
        // 缩放控件
        this.mapUIOperateModel.getScaleView()
            .setShow(false) 
        // 比例尺控件
        this.mapUIOperateModel.getZoom()
            .setShow(false)  // 是否显示
    })

Button("改变位置", { type: ButtonType.Capsule, stateEffect: true }).onClick(() => {
         // 比例尺控件
         this.mapUIOperateModel.getZoom()
            .setShow(true)  // 是否显示
            .setAlignment(Alignment.BottomEnd)  // 对齐方式
            .setY('-200px')  // y方向距离
         // 缩放控件
         this.mapUIOperateModel.getScaleView()
            .setShow(true)
            .setAlignment(Alignment.BottomStart)
            .setY('-200px')
    }).borderRadius(8)
      .backgroundColor(0x317aff)
      .margin(5)

MapComponent({
    onReady: (err, controller) => {
       if (!err) {
         this.mapController = controller
       }
     }, mapOptions: this.mapOpt, mapUIOperate: this.mapUIOperateModel
}).width('100%').height('100%')        
```

#### 引擎类型控件

目前支持指北针控件、定位图标控件的属性设置。

**指北针**

可以设置显示位置、是否显示

```typescript
this.mapController.mapStatus.setRotate(30).setCenterPoint(new LatLng(30, 112)).refresh();
this.compass = this.mapController.getLayerByTag(SysEnum.LayerTag.COMPASS) as CompassLayer;
this.compass && (this.compass.x = 64);
this.compass && (this.compass.y = 64);
// 设置显示/隐藏
// this.compass && (this.compass.visible = true);
```

**定位图标**

可以设置显示位置、是否显示以及图标指向、扩散范围

```typescript
 let result = this.mapController.getLayerByTag(SysEnum.LayerTag.LOCATION);
if(result){
    // 设置定位图标位置、指向以及范围
    this.loc = result as LocationLayer;
    this.loc.location = new LatLng(30, 112);
    this.loc.direction = 90;
    // 单位米
    this.loc.radius = 1000;
}
```

### 方法交互

根据场景的不同可以分别通过[MapStatus](https://lbsyun.baidu.com/api/harmony?title=harmonynextsdk/guide/interaction/method#MapStatus)的方法或者[MapController](https://lbsyun.baidu.com/api/harmony?title=harmonynextsdk/guide/interaction/method#MapController)的方法改变地图状态。

#### 显示位置设置

```typescript
mapController.mapStatus.centerPoint = new LatLng(30, 112);
mapController.setMapCenter(new LatLng(30, 112));
```

#### 显示级别设置

注意：当设置的地图缩放级别超出SDK支持的最大或最小级别时对应以最大或最小缩放级别显示。

```typescript
// 直接缩放至缩放级别16
mapController.mapStatus.level = 16;
// 缩放到指定等级
mapController.zoomTo(16);
// 放大地图一级
mapController.zoomInOne();
// 缩小地图一级
mapController.zoomOutOne();
```

#### 设置地图最佳视野

```typescript
// 通过坐标序列点形式
this.mapController.setViewport(
[
  new LatLng(39.912935, 116.433119),
  new LatLng(39.412935, 115.433119),
  new LatLng(39.412935, 116.433119),
  new LatLng(39.912935, 115.433119)
],{
margins:[vp2px(100),vp2px(100),vp2px(100),vp2px(100)]
});

// 通过Bounds形式
this.mapController.fitVisibleMapRect(
    new Bounds(new LatLng(39.412935, 115.433119),new LatLng(39.912935, 116.433119)),
    new WinRound(vp2px(100),vp2px(100),vp2px(100),vp2px(100)),
    true
);
```

### 事件交互

地图事件主要包括地图状态事件、地图手势事件事件。

#### 地图状态事件监听

```typescript
mapController.addEventListener(MapEvent.MAPSTATUSCHANGESTART, () => {
  console.log('MapEvent.MAPSTATUSCHANGESTART');
});

mapController.addEventListener(MapEvent.MAPSTATUSCHANGE, () => {
  console.log('MapEvent.MAPSTATUSCHANGE');
});

mapController.addEventListener(MapEvent.MAPSTATUSCHANGEFINISH, () => {
   // 获取地图四至范围 
  console.log('MapEvent.MAPSTATUSCHANGEFINISH', mapController.mapStatus.getGeoRound());
});
```

#### 地图手势事件监听

```typescript
// 点击事件
 this.mapController.addEventListener(MapEvent.CLICK, (event:TMapViewEvent) => {
    // 必须转换类型才能使用 
    event = event as EventBundle;
    const marker:Marker = new Marker({
        position: event.geo,
        icon: image
    });
    this.mapController?.addOverlay(marker);
});

// 双击事件
this.mapController.addEventListener(MapEvent.DOUBLECLICK, (event:TMapViewEvent) => {
    // 必须转换类型才能使用 
    event = event as EventBundle;
    let left = event.left.toFixed();
    let top = event.top.toFixed();
});

this.mapController.addEventListener(MapEvent.PINCHSTART, (event:TMapViewEvent) => {
     console.log('缩放事件开始');
});

this.mapController.addEventListener(MapEvent.PINCHUPDATE, (event:TMapViewEvent) => {
    console.log('缩放事件过程中');
});

this.mapController.addEventListener(MapEvent.PINCHEND, (event:TMapViewEvent) => {
    console.log('缩放事件结束');
});

this.mapController.addEventListener(MapEvent.ROTATIONSTART, (event:TMapViewEvent) => {
    console.log('旋转事件开始');
});

this.mapController.addEventListener(MapEvent.ROTATIONUPDATE, (event:TMapViewEvent) => {
    // 必须转换类型才能使用 
    event = event as EventBundle;
    let rotationAngle = event.rotationAngle??0;
    console.log('旋转事件过程中',rotationAngle);
});

this.mapController.addEventListener(MapEvent.ROTATIONEND, (event:TMapViewEvent) => {
    console.log('旋转事件结束');
});

this.mapController.addEventListener(MapEvent.TOUCHSTART, (event:TMapViewEvent) => {
    console.log('移动事件开始');
});

this.mapController.addEventListener(MapEvent.TOUCHMOVE, (event:TMapViewEvent) => {
    console.log('移动事件过程中');
});

this.mapController.addEventListener(MapEvent.TOUCHEND, (event:TMapViewEvent) => {
    console.log('移动事件结束');
});
```

#### 底图poi、定位图标点击回调

```typescript
class myClickListener implements IMapClickListener {
    /**
       * 一般情况下的点击回调（定位图标、指南针、底图的 poi 点等）
       * @param mapObjArray
   */
    onClickedMapObj(arrClickObjs: Array<MapClickObj>){
      arrClickObjs.map((obj:MapClickObj)=>{
        console.log('点击了--',obj.strText)
      })
    };
}

const listener = new myClickListener()
this.mapController.setMapClickListener(listener)
```

## 2. 覆盖物绘制（模块：map）

> 模块：`@bdmap/map`　docs：`api/modules/map.md`　常用检索词：Marker / Polyline / Polygon / Circle / Label / PopView / ClusterGroup / Track / HeatMapBuilder / ImageTileLayer / Prism / Building / Bd_3DModel

### 介绍（地图覆盖物）

地图覆盖物是地理信息可视化中的关键元素，通过叠加于基础地图之上的特定图形或交互组件，实现数据标注、区域划分、立体展示及信息交互等功能。

### 覆盖物分类

覆盖物组合使用可构建多层次、高交互的地图应用，满足从基础标注到复杂分析的多样化需求。以下为常见覆盖物分类及特性说明：

1.点状覆盖物

**Marker（标记点）：**以图标形式标注特定位置（如景点、设施、目的地），支持自定义图标样式、尺寸及点击事件。

**Label（文本标签）：**以文字信息标注特定位置，用于补充说明（如名称、距离），可调整字体、颜色及位置偏移。

2.线性覆盖物

**Polyline（折线）：**连接多个坐标点形成连续路径，常用于表示路线、轨迹或边界线。支持设置线宽、颜色及虚线样式。

3.面状覆盖物

**Polygon（多边形）：**由闭合折线构成的封闭区域，用于标注行政区划、兴趣范围等，可填充颜色并设置透明度。

**Circle（圆形）：**以中心点和半径定义的圆形区域，适用于覆盖范围标注（如服务半径）。

**Ground（地面覆盖）：**通过纹理或颜色填充特定区域（如水域、绿地），增强地图层次感。

4.立体覆盖物

**Prism（棱柱体）：**基于Polygon生成的3D柱状结构，用于展示高度数据（如建筑群）。

**Building（模型建筑）：**加载3D模型或简模，实现城市级建筑群可视化，支持调整高度、材质等属性。

5.信息交互组件

**PopView（信息弹窗）：**覆盖物点击后触发的浮层窗口，可嵌入文本、图片或自定义UI内容，提供详细数据展示与操作入口。

### 覆盖物基础能力

覆盖物基础能力覆盖了**交互事件**、**动态显示**、**样式配置**和**数据扩展**四大核心场景，支持通过链式调用（如alpha().clickable()）实现灵活配置。

1.事件交互能力

**事件监听：**通过addEventListener支持绑定点击（CLICK）、触摸（TOUCH）等交互事件。

**事件移除：**通过removeEventListener动态解绑事件，避免内存泄漏。

**点击控制：**clickable方法控制覆盖物是否可触发交互事件。

2.显示控制能力

**显隐切换：**通过visible属性和setVisible方法动态显示或隐藏覆盖物。

**层级管理：**zIndex和setZIndex控制覆盖物的叠加顺序，避免遮挡问题。

**条件显示：**startLevel和endLevel定义覆盖物在地图缩放层级范围内的显示条件。

3.样式配置能力

**透明度调节：**alpha和setAlpha支持透明度动态调整（范围为[0, 1]）。

**属性扩展：**setExtraInfo允许附加自定义数据（如业务ID、标签等），增强覆盖物的信息承载能力。

### 绘制Marker点

Marker标记支持添加、移除、点击事件等。

### 添加移除Marker

[Marker](https://lbsyun.baidu.com/api/harmony?title=harmonynextsdk/guide/render-map/point#Marker)的 icon图标通过[ImageEntity](https://lbsyun.baidu.com/api/harmony?title=harmonynextsdk/guide/render-map/point#ImageEntity)对象设置。

```typescript
import { MapController, Marker, ImageEntity } from '@bdmap/map';
import { LatLng } from '@bdmap/base';
mapController: MapController |null = null

let marker = new Marker({
    position: new LatLng(39.904835, 116.403119),
    icon: new ImageEntity("rawfile://marker.png"),
    // [⚠️注意] 方位设置，无特殊说明，使用默认值
    located: SysEnum.Located.TOP
});

// 在地图上添加Marker，并显示
this.mapController?.addOverlay(marker);

// 移除Marker
this.mapController?.removeOverlay(marker);
```

### 事件定义

```typescript
import { OverlayEvent, Marker,TMapViewEvent,EventBundle } from '@bdmap/map';

marker: Marker | null = null;

this.marker?.addEventListener(OverlayEvent.CLICK, (e:TMapViewEvent) => {
    // 必须转换类型才能使用 
    let result = e as EventBundle;
    console.log('EVENT handleTouchSingle===click marker1 ',result.geo.toString());
});
```

### 碰撞策略

碰撞策略通过枚举[CollisionBehavior](https://lbsyun.baidu.com/api/harmony?title=harmonynextsdk/guide/render-map/point#CollisionBehavior)设置，锚点位置通过枚举[Located](https://lbsyun.baidu.com/api/harmony?title=harmonynextsdk/guide/render-map/point#Located)设置。

```typescript
import { MapController, Marker, ImageEntity, SysEnum } from '@bdmap/map';
import { LatLng } from '@bdmap/base';

mapController: MapController | null = null;

let marker = new Marker({
    position: new LatLng(39.904835,116.403119),
    isJoinCollision: SysEnum.CollisionBehavior.NOT_COLLIDE,
    located: SysEnum.Located.TOP,
    icon: new ImageEntity('rawfile://bg.png')
});

this.mapController?.addOverlay(marker);
```

### 添加信息框

从2.0.0版本开始，不再支持InfoWindow覆盖物类型，请使用PopView进行信息框开发。

有两种设置Marker信息框的方式：一种是附加 InfoWindow 形式，一种是附加[PopView](https://lbsyun.baidu.com/api/harmony?title=harmonynextsdk/guide/render-map/point#PopView)的形式。

推荐使用第二种方式，UI形式更加灵活，功能更加全面。

**第一种**

```typescript
let infoWin = new InfoWindow({
    anchorX: 0.5,
    anchorY: 0,
    content: new ImageEntity(pixmap,width,height)
})

infoWin.addEventListener(OverlayEvent.CLICK,()=>{
    promptAction.showToast({
        message: '信息框点击',
        duration: 2000,
    });
});

this.marker?.setInfoWindow(infoWin);
```

**第二种**

```typescript
import { MapController, Marker, ImageEntity, SysEnum, LabelUI, CommonEvent, TextStyle, PopView } from '@bdmap/map';

mapController: MapController | null = null;
marker: Marker | null = null;

let image = new ImageEntity('rawfile://start.png');
this.marker = new Marker({
    position: new LatLng(39.904835, 116.403119),
    icon: image,
    located: SysEnum.Located.BOTTOM
});

/** PopView */
{
    let layout = new HorizontalLayout();
    layout.setBackground(new ImageEntity("rawfile://pop_bottom.png"),{
        scaleX: [20,40,100,120],
        scaleY: [40,80],
        fillArea: [20,120,20,80]
    })
    let label = new LabelUI();
    label.setGravity(SysEnum.Gravity.GRAVITY_CENTER);
    label.setText("#BmMarker# 百度地图");
    label.setBackgroundColor('rgba(255,235,59,0.5)');
    label.setPadding(20, 0, 0, 0);
    label.setClickable(false);
    label.addEventListener(CommonEvent.CLICK,(e:EventUIBundle)=>{
    })
    let txtStyle =  new TextStyle();
    txtStyle.setTextColor('rgba(255,0,255,1)');
    txtStyle.setTextSize(28);
    txtStyle.setFontOption(SysEnum.FontOption.BOLD);
    label.setStyle(txtStyle);
    layout.addView(label);
    let popView = this.popView = new PopView();
    popView.setVisibility(SysEnum.Visibility.VISIBLE);
    popView.setView(layout);
    popView.setLocated(SysEnum.Located.TOP);
    popView.addEventListener(CommonEvent.CLICK,(e:EventUIBundle)=>{
    })
    // 附加PopView
    this.marker?.setPopView(popView);
}
this.mapController?.addOverlay(this.marker);
```

### 同时添加大量覆盖物性能优化问题

**一、图片资源预先处理**

使用ImageEntity对象时，可首先通过getBitmap()判断是否已经存在图像解析资源，如果不存在，则通过getArrayBuffer(callback?: Callback<ArrayBuffer>)进行生成后，再使用此对象。如果存在多个ImageEntity对象，则参考下面fetchAllImages示例代码逻辑进行处理。

```typescript
fetchAllImages(input:ImageEntity|Array<ImageEntity>,callback: Function){
    let imageList:Array<ImageEntity> = Array.isArray(input)?input:[input];
    let proList: Array<Promise<void>> = [];
    imageList.forEach(item=>{
      let pro = new Promise<void>((resolve,reject)=>{
        if(!item.getBitmap()){
          item.getArrayBuffer(()=>{
            resolve();
          })
        }else{
          resolve();
        }
      });
      proList.push(pro);
    });
    Promise.all(proList).then(()=>{
      callback.bind(this)();
    });
  }
```

**二、减少地图渲染更新频率**

数据添加到地图前，可通过使用OverlayLayer图层对象的pauseCommit()暂停主动提交对象渲染更新，当数据添加完毕后，再通过resumeCommit()恢复主动提交对象渲染更新。

**三、示例代码**

```typescript
mainTask(){
    this.image = new ImageEntity('rawfile://your-image-url.png');
    this.fetchAllImages(this.image,()=>{
        this.addMarker();
    });
}

addMarker(){
    if(!this.mapController){
      return;
    }
    let overlayLayer = this.mapController.getOverlayLayer();
    overlayLayer.pauseCommit();
    let lng = 116.403119;
    for(let i = 30; i>0;i--){
      for(let j = 30; j>0;j--) {
        let marker = new Marker({
          position: new LatLng(39.904835 + i * 0.05, lng + j * 0.05),
          icon: this.image as ImageEntity
        });
        this.mapController?.addOverlay(marker);
      }
    }
    overlayLayer.resumeCommit();
  }
```

### Marker拖动交互

操作流程：长按Marker触发拖动开始；移动手指到目标位置；抬起手指，完成拖放。

具体通过setDraggable(enable:Boolean)方法设置是否允许被拖动，通过addDragListener(listener:OverlayDragListener)方法设置Marker拖动回调事件。

参考示例代码如下：

```typescript
@Component
export struct DraggableMarker {
    mapController: Maybe<MapController>;
    points: Array<LatLng> = [new LatLng(39.95033459580572,116.38188371611014), new LatLng(39.99449376883313,116.38314134382411)];
    markers: Array<Marker> = [];

    showMarker(){
        if(!this.mapController) return;
        this.markers = this.points.map((point, index) => {
          let marker = new Marker({
            position: point
          })
          marker.addDragListener(new MarkerDrag());
          this.mapController?.addOverlay(marker);
          return marker;
        })
    }

    changeEnableDrag(enable: boolean) {
        this.markers.forEach(marker => {
          marker.setDraggable(enable);
        })
    }

    build() {
        Stack({ alignContent: Alignment.TopStart }) {
          Column() {
            Row() {
              Button('可拖动', { type: ButtonType.Capsule, stateEffect: true })
                .onClick(() => {
                  this.changeEnableDrag(true);
                }).borderRadius(8)
                .backgroundColor(0x317aff)
                .margin(5)
              Button('不可拖动', { type: ButtonType.Capsule, stateEffect: true })
                .onClick(() => {
                  this.changeEnableDrag(false);
                }).borderRadius(8)
                .backgroundColor(0x317aff)
                .margin(5)
            }
            Row(){
              Text("长按地图上的Marker，图标变大后开始拖动，拖到目标位置，抬起手指，完成Marker拖动").margin(5).fontSize(12)
            }
          }.zIndex(10).width('100%').backgroundColor('#f3f3f3').justifyContent(FlexAlign.Center)

          MapComponent({
            onReady: (e, mapController: MapController) => {
              if (mapController) {
                this.mapController = mapController;
                this.showMarker();
              }
            },
           mapOptions: new MapOptions({
              mapStatus: new MapStatus({
                center: new LatLng(39.97033459580572, 116.38188371611014),
                zoom: 14
              })
            })
          }).width('100%').height('100%')
        }.width('100%').height('100%')
      }
 }

export class MarkerDrag implements OverlayDragListener {
  dragStart(overlay: Marker, ev: OverlayDragEvent) {
    console.log('MarkerDrag::dragStart');
    overlay.setScale(2,2);
  }
  dragMove(overlay: Marker, ev: OverlayDragEvent) {
    console.log('MarkerDrag::dragMove', JSON.stringify(ev));
  }
  dragEnd(overlay: Marker, ev: OverlayDragEvent) {
    console.log('MarkerDrag::dragEnd');
    overlay.setScale(1,1);
  }
}
```

### 点聚合

### 使用流程

1) 准备 Map与Controller

通过MapComponent的onReady获取mapController

2) 构建聚合 UI

用ClusterText+TextStyle设置文字
用ClusterIcon+ImageEntity设置图标
用ClusterTemplate.setClusterUI组合 UI

3) 创建聚合组并加入地图

newClusterGroup(template, opt)，再mapController.addOverlay(group)

4) 批量创建Marker并加入聚合组

每个Marker指定position: LatLng与icon: ImageEntity

### 最小可用示例

```typescript
import {
  MapComponent, MapController, MapOptions, MapStatus, LatLng,
  ClusterGroup, ClusterTemplate, ClusterText, ClusterIcon,
  TextStyle, ImageEntity, Marker
} from '@bdmap/map_walkride_search';

let mapController: MapController | null = null;

const mapOptions: MapOptions = new MapOptions({
  mapStatus: new MapStatus({
    center: new LatLng(39.94923, 116.397428),
    zoom: 13,
    overlook: 30
  })
});

// onReady 拿到 controller
// mapController = ...

function addCluster(): void {
  // 1) 准备 UI 组件
  const clusterIconImg: ImageEntity = new ImageEntity("rawfile://icon_cat.png");
  const markerIcon: ImageEntity = new ImageEntity("rawfile://poicity.png");
  const clusterText: ClusterText = new ClusterText(0);
  const clusterTextStyle: TextStyle = new TextStyle();
  clusterTextStyle.setTextSize(5);
  clusterText.build("test", clusterTextStyle);
  const clusterIcon: ClusterIcon = new ClusterIcon(1);
  clusterIcon.build(clusterIconImg);
  const template: ClusterTemplate = new ClusterTemplate();
  template.setClusterUI([clusterText, clusterIcon]);

  // 2) 创建聚合组并添加到地图
  const group: ClusterGroup = new ClusterGroup(template, {
    zIndex: 1,
    alpha: 0,
    visible: true,
    isClickable: false,
    startLevel: 4,
    endLevel: 22
  });
  mapController?.addOverlay(group);

  // 3) 批量创建 Marker 并加入聚合
  const startLat: number = 39.865397;
  const startLng: number = 115.826785;
  for (let i = 0; i < 10; i++) {
    for (let j = 0; j < 10; j++) {
      const mark: Marker = new Marker({
        position: new LatLng(startLat + j * 0.05, startLng + i * 0.05),
        icon: markerIcon
      });
      group.addMarker(mark);
    }
  }
}
```

### Marker点动画

### Marker帧动画

自2.0.3版本起，SDK提供了给Marker增加帧动画的功能，一次传入一个Icon列表，通过interval设定刷新的帧间隔。

示例代码如下：

```typescript
const images = [new ImageEntity("rawfile://icon_marka.png"),new ImageEntity("rawfile://icon_markb.png"),new ImageEntity("rawfile://icon_markc.png")]
this.marker = new Marker({
  position: new LatLng(39.904835, 116.403119),
  icons: images, 
  interval: 160
});
this.mapController?.addOverlay(this.marker)
```

运行结果如下：

### Marker动画

除了可以自定义的帧动画，Marker还支持设置旋转、缩放、平移、透明、和组合动画效果。通过Marker类setAnimation方法设置。

| Transformation | 平移 |
| RotateAnimation | 旋转 |
| ScaleAnimation | 缩放 |
| SingleScaleAnimation | X 或 Y 轴方向单独缩放 |
| AlphaAnimation | 透明 |
| AnimationSet | 动画集合 |

平移动画效果的示例代码如下：

```typescript
getTransformation():Transformation {
    const latLngA = new LatLng(39.904835, 116.403119);
    const latLngB = new LatLng(40, 116.403);
    const transformation = new Transformation([latLngA,latLngB]);
    transformation.setDuration(1000);// 设置动画时间
    transformation.setRepeatMode(SysEnum.MarkerRepeatMode.REVERSE);// 动画重复模式
    transformation.setRepeatCount(1);// 动画重复次数
    return transformation;
}
const animation = this.getTransformatio()
this.marker.setAnimation(animation);
animation.start();
```

### 加载Marker时增加动画

SDK提供了加载Marker时的动画效果，有如下四种效果供开发者选择：

| AnimateDefine.NONE | 无效果 |
| AnimateDefine.DROP | 从天上掉下 |
| AnimateDefine.GROW | 从地下生长 |
| AnimateDefine.JUMP | 跳跃 |

通过IMarkerOption中的animateType属性设置。

DROP动画示例代码如下：

```typescript
let image: ImageEntity = new ImageEntity("rawfile://map_marker_red.png");
this.marker = new Marker({
  position: new LatLng(39.904835, 116.403119),
  icon: image,
  located: SysEnum.Located.CENTER,
  animateType: SysEnum.AnimateDefine.DROP  // 设置动画类型
});
this.mapController.addOverlay(this.marker);
```


### 绘制线

线类覆盖物支持在地图上绘制折线、虚线、带纹理的线，通过这些可以绘制各种各样的规划路线或物体轨迹。

### 绘制折线

通过Polyline类会来绘制折线，示例代码如下：

```typescript
polyline = new Polyline({
     points: [new LatLng(39.76, 116.13),
          new LatLng(39.95, 116.23),
          new LatLng(40.16, 116.78)],
     fillcolor: '#f0f',
     width: 20,
     join: SysEnum.LineJoinType.ROUND,
     cap: SysEnum.LineCapType.ROUND,
     isThined: true,
});
mapController.addOverlay(polyline);
```

### 绘制多段颜色折线

通过设置colorList即可实现多段颜色的设置，colorList长度需要比points长度小1。

```typescript
this.colorsLine = new Polyline({
    points: [new LatLng(39.620, 116.327), new LatLng(39.9171, 116.522),new LatLng(39.8171, 116.622),new LatLng(40.36, 116.43), new LatLng(40.77, 115.78)],
    width: 20,
    join: SysEnum.LineJoinType.ROUND,
    cap: SysEnum.LineCapType.BUTT,
    colorList: ['#f0f', '#3c6e04', '#b31203','#f0f']
});
```

### 绘制渐变颜色折线

通过isGradient参数设置是否是渐变线，colorList长度需要与points长度一致。

```typescript
this.gradientLine = new Polyline({
    points: [new LatLng(39.620, 116.327), new LatLng(39.9171, 116.522),new LatLng(39.8171, 116.622),new LatLng(40.36, 116.43), new LatLng(40.77, 115.78)],
    width: 20,
    join: SysEnum.LineJoinType.ROUND,
    cap: SysEnum.LineCapType.BUTT,
    isGradient: true,
    colorList: ['#f0f', '#3c6e04', '#b31203','#f0f','#3c6e04']
});
this.gradientLine.addEventListener(OverlayEvent.CLICK,()=>{
    // 设置为非渐变模式 
    this.gradientLine?.colorList(['#f0f', '#3c6e04', '#b31203','#f0f']).setIsGradient(false);
});
```

### 绘制虚线

通过dottedline和dottedlineType参数配置，可实现虚线样式绘制。

示例代码：

```typescript
dotline = new Polyline({
    points: [new LatLng(39.620, 116.327), new LatLng(39.9171, 116.522)],
    fillcolor: '#00f',
    width: 20,
    join: SysEnum.LineJoinType.ROUND,
    cap: SysEnum.LineCapType.BUTT,
    dottedline: true,
    dottedlineType: SysEnum.PolylineDottedLineType.DOTTED_LINE_CIRCLE
});
// 在地图中添加点状虚线
mapController.addOverlay(dotline);
```

效果图：

### 绘制带纹理折线

示例代码：

```typescript
polylineGeodesic = new Polyline({
     points: [new LatLng(40.082, 116.617),
          new LatLng(55.851, 37.701),
          new LatLng(32.851, 112.701)],
     fillcolor: '#ff10bed6',
     width: 16,
     join: SysEnum.LineJoinType.ROUND,
     cap: SysEnum.LineCapType.ROUND,
     textures: [new ImageEntity('rawfile://Icon_road_blue_arrow.png')], // 添加纹理
     isThined: false,
     isGeodesic: true // 是否绘制大地线
});
mapController.addOverlay(polylineGeodesic);
```

效果图：

### 绘制多纹理折线

通过配置textures参数，设置多纹理数据；通过配置indexList配置每段线的纹理索引。indexList数组的长度比points数组长度小1，且indexList数组中的每个数值取值范围为0至textures的长度减1。

```typescript
let trace = [
    new LatLng(39.88063,116.47946),
    new LatLng(39.88063,116.47951),
    new LatLng(39.88099,116.47951),
    new LatLng(39.88126,116.47951),
    new LatLng(39.88158,116.4795),
    new LatLng(39.88158,116.4795),
    new LatLng(39.88234,116.4795),
    new LatLng(39.88234,116.4794),
    new LatLng(39.88232,116.47925),
    new LatLng(39.88232,116.47913),
    new LatLng(39.88228,116.47838),
    new LatLng(39.88296,116.4774),
    new LatLng(39.88433,116.47741),
    new LatLng(39.88505,116.47742),
    new LatLng(39.8901,116.4775),
    new LatLng(39.89215,116.47755),
    new LatLng(39.89469,116.47831),
    new LatLng(39.89463,116.4787)];

this.polyline = new Polyline(
    {
        points: trace,
        width: 30,
        join: SysEnum.LineJoinType.ROUND,
        cap: SysEnum.LineCapType.ROUND,
        textures:[new ImageEntity('rawfile://Icon_road_blue_arrow.png'),
            new ImageEntity('rawfile://Icon_road_green_arrow.png'),
            new ImageEntity('rawfile://Icon_road_red_arrow.png'),
            new ImageEntity('rawfile://Icon_road_yellow_arrow.png')], // 添加纹理图片
        indexList:[1,1,1,1,2,2,3,3,1,1,1,2,2,1,1,1,1], // 填充多纹理的索引，数量等于点数减1
    });
this.polyline.addEventListener(OverlayEvent.CLICK, () => {
    promptAction.showToast({
        message: '点击多纹理线',
        duration: 2000,
    });
});
this.mapController?.addOverlay(this.polyline);
this.mapController?.setViewport(trace,{margins:[vp2px(100),vp2px(100),vp2px(100),vp2px(100)]})
```

### Bloom效果折线

通过配置lineBloomType、lineBloomWidth、lineBloomBlurTimes、lineBloomAlpha来实现Bloom发光特效。

```typescript
// 方形虚线
this.lineBloom = new Polyline({
    points: [new LatLng(39.420, 116.237), new LatLng(40, 116.822),new LatLng(39.9171, 116.522)],
    fillcolor: '#62d',
    width: 16,
    join: SysEnum.LineJoinType.ROUND,
    cap: SysEnum.LineCapType.BUTT,
    lineBloomType: SysEnum.ELineBloomType.GRADIENTA,
    lineBloomWidth: 50,
    lineBloomBlurTimes: 1,
    lineBloomAlpha: 0.5,
});
this.mapController.addOverlay(this.lineBloom);
```

### Track动画能力

通过TrackAnimation设置轨迹线动画效果

1. 创建TrackAnimation动画，并绑定到Polyline

```typescript
const polyline = new Polyline({
    points: trackList, // 轨迹线坐标数组LatLng[]
    fillcolor: 'rgba(71, 205, 22, 1.0)',
    width: 6,
    strokeWidth: 2,
    strokeColor: 'rgba(8, 32, 150, 1.00)',
    collisionBehavior:SysEnum.CollisionBehavior.COLLIDE_WITH_BASEPOI
});

let trackAnimate = this.trackAnimate = new TrackAnimation(trackList);
// trackAnimate.setDuration(1000);
// trackAnimate.setTrackPosRadio(1.0, 0.0);
trackAnimate.setTrackPos(trackList[0]);
trackAnimate.setTrackLine(polyline);
// 设置轨迹动画运行中实时返回的绑路轨迹点以及方向
trackAnimate.setTrackUpdateListener({
    onTrackUpdate: (pt: LatLng, fAngle: number, fPathFraction: number)=>{
        console.log('TrackAnimation',pt,fAngle,fPathFraction);
    }
})
polyline.setCollisionBehavior(SysEnum.CollisionBehavior.ALWAYS_SHOW)
polyline.setAnimation(trackAnimate);
this.mapController.addOverlay(polyline);
// [必须]2.0.3版本及之前需要立即调用一次pause方法，防止onTrackUpdate回调点跳跃问题
trackAnimate.pause();
```
2. [可选] 设置动画线样式
```typescript
  //  设置未经过线样式
  let forwardStyle = new LineStyle();
  forwardStyle.setWidth(12);
  // forwardStyle.setStrokeColor(Color.Gray);
  // forwardStyle.setStrokeWidth(6);
  forwardStyle.setBitmapResource(new ImageEntity('rawfile://Icon_road_green_arrow.png'))
  polyline.setTrackForwardStyle(forwardStyle);
  // 设置已经过线样式
  let backwardStyle = new LineStyle();
  b backwardStyle.setWidth(12);
  // backwardStyle.setColor(Color.White);
  // backwardStyle.setStrokeColor(Color.Gray);
  // backwardStyle.setStrokeWidth(6);
  backwardStyle.setBitmapResource(new ImageEntity('rawfile://Icon_road_blue_arrow.png'))
  polyline.setTrackBackwardStyle(backwardStyle);
```

3. 启动动画

```typescript
// point为实时轨迹点
this.trackAnimate.setTrackPos(point); // 轨迹点，也可以使用setTrackPosRadio占比表达
this.trackAnimate.setDuration(1000);
// [必须]start配合setDuration使用
this.trackAnimate.start()
```

### 绘制弧线

弧线由Arc类定义，一条弧线由起点、中点和终点三个点确定位置。开发者可以通过IArcOption设置弧线的位置，宽度和颜色。

### arc覆盖物参数配置

| color | number | 否 | 线颜色（ARGB 整数） |
| width | number | 否 | 线宽（像素） |
| startPoint | LatLng | 是 | 起点坐标，可与 middlePoint、endPoint一起定义圆弧 |
| middlePoint | LatLng | 是 | 中点坐标，用于确定圆弧方向与圆心 |
| endPoint | LatLng | 是 | 终点坐标，与起点、中点共同定义圆弧 |
| pixelRadius | number | 否 | 像素半径 |

### 示例代码

示例代码如下：

```typescript
const arc = new Arc({
    startPoint: new LatLng(39.97923, 116.357428),
    middlePoint: new LatLng(39.94923, 116.397428),
    endPoint: new LatLng(39.97923, 116.437428),
    width: 10,
    isClickable: true,
});
//在地图上显示弧线
this.mapController?.addOverlay(arc)
```

### 绘制面

多边形是一组Latlng点按照传入顺序连接而成的封闭图形，开发者可以通过Polygon设置多边形的位置、边框和填充颜色。

### 示例代码

```typescript
// 添加多边形覆盖物
let pathArr: LatLng[] = [
    new LatLng(39.9122, 116.2575),
    new LatLng(40.0191, 116.4624),
    new LatLng(39.913506, 116.4955)
];
 let opts:IPolygonOption = {
    points: pathArr,
    fillcolor:\'#0f0\',
    stroke: new Stroke({
        strokeWidth: 12,
        color: \'#ff00dd\',
        strokeStyle: SysEnum.StrokeStyle.SQUARE
    })
}
this.polygon = new Polygon(opts);
this.polygon.setPoints(pathArr);
this.polygon.setFillcolor(\'#f9f\');
this.polygon.addEventListener(OverlayEvent.CLICK, () => {
    this.polygon?.setFillcolor(\'rgba(0,0,255,0.6)\');
    promptAction.showToast({
        message: \'点击多边形\',
        duration: 2000,
    });
});
this.mapController.addOverlay(this.polygon);
```

### 绘制AOI检索图形

```typescript
AoiSearch.newInstance().requestAoi({
    latLngList: [new LatLng(40.070754, 116.324175)]
})
.then((res: AoiResult) => {
    if (res) {
        if (res.aoiList) {
            for (let item of res.aoiList) {
                if(item.polygon){
                    let aoi_poly = new Polygon({
                        points: item.polygon,
                        fillcolor: \'#ff0000\',
                        alpha: 0.5
                    })
                    this.mapController.addOverlay(aoi_poly)
                }
            }
        }
    }
})
```

### 绘制文字

可以在地图上叠加自定义文字，由[Label](https://lbsyun.baidu.com/api/harmony?title=harmonynextsdk/guide/render-map/text#Label)类定义，效果图如下：

### 示例代码如下：

```typescript
 // 添加文字标注
let label = new Label();
label.text("百度地图\\3S").fontSize(32).position(new LatLng(36.925, 113.4013)).bgcolor("rgba(255,235,59,0.5)").setFontColor("rgba(255,0,255,1)");
this.mapController.addOverlay(label);

// 添加文字标注
let label2 = new Label();
label2.text("百度地图\\4S").fontSize(32).position(new LatLng(36.625, 113.4013)).fontType(Label.BOLD).bgcolor("rgba(255,235,59,0.6)").setFontColor("rgba(255,0,255,1)");
this.mapController.addOverlay(label2);

// 添加文字标注
let label3 = new Label();
label3.text("百度地图\\5S").fontSize(32).position(new LatLng(36.425, 113.4013)).fontType(Label.BOLD_ITALIC).bgcolor("rgba(255,235,59,0.8)").setFontColor("rgba(8, 18, 203, 1.00)");
this.mapController.addOverlay(label3);

// 添加文字标注
let label4 = new Label();
label4.text("百度地图\\6S").fontSize(32).position(new LatLng(36.225, 113.4013)).fontType(Label.ITALIC).bgcolor("rgba(255,235,59,1)").setFontColor("rgba(1, 55, 10, 1.00)");
this.mapController.addOverlay(label4);

// 改变文字颜色
this.mapController.addOverlayEventListener(EOverLayTypeName.LABEL,OverlayEvent.CLICK,(bundle:EventOverlayBundle)=>{
    let labels = bundle.target as Array<Overlay>;
    if(labels && labels.length>0){
        labels.forEach(item=>{
            if(item instanceof Label){
                item.setFontColor("#000");
                promptAction.showToast({
                    message: "点击文字",
                    duration: 2000,
                });
            }
        });
    }
});
}
```

### 添加信息窗

可以在地图上叠加自定义文字,由[PopView](https://lbsyun.baidu.com/api/harmony?title=harmonynextsdk/guide/render-map/text#PopView)类定义

示例代码如下：

```typescript
import { MapController, Label, LabelUI, TextStyle, SysEnum, PopView } from '@bdmap/map';
import { LatLng } from '@bdmap/base';

mapController: MapController | null = null;

let label = new Label({
     position: new LatLng(39.904835, 116.403119),
     located: SysEnum.Located.BOTTOM,
     text: '公园',
     fontsize: 35,
     fontcolorstr: 'rgba(255,0,255,1)'
});

/** PopView */
{
    let layout = new HorizontalLayout();
    layout.setBackground(new ImageEntity("rawfile://pop_bottom.png"),{
    /** 横向可缩放区域 [x1,x2] or [x1,x2,x3,x4] @since 1.2.0*/
     scaleX: [20,40,100,120],
    /** 纵向可缩放区域 [y1,y2] or [y1,y2,y3,y4]  @since 1.2.0*/
     scaleY: [40,80],
    /**「.9」的内容区域 [x1,x2,y1,y2]  @since 1.2.0*/
     fillArea: [20,120,20,80]
    })
    layout.setGravity(SysEnum.Gravity.CENTER)
    let labelUI = new LabelUI();
    labelUI.setGravity(SysEnum.Gravity.GRAVITY_CENTER);
    // 提示信息设置
    labelUI.setText("######休闲散步公园#");             
    labelUI.setBackgroundColor('rgba(255,235,59,0.5)')
    labelUI.setPadding(20, 0, 0, 0);
    labelUI.setClickable(false);
    labelUI.addEventListener(CommonEvent.CLICK,(e:EventUIBundle)=>{
    })
    let txtStyle =  new TextStyle();
    txtStyle.setTextColor('rgba(255,235,59,0.5)');
    txtStyle.setTextSize(28);
    txtStyle.setFontOption(SysEnum.FontOption.BOLD);
    labelUI.setStyle(txtStyle);
    layout.addView(labelUI);
    let popView = new PopView();
    popView.setVisibility(SysEnum.Visibility.VISIBLE);
    popView.setView(layout);
    popView.setLocated(SysEnum.Located.TOP);
    popView.addEventListener(CommonEvent.CLICK,(e:EventUIBundle)=>{
    })
    // 附加PopView
    label.setPopView(popView);
}
this.mapController?.addOverlay(label);
```

### 绘制圆

圆由Circle类定义，开发者可以通过CircleOptions类设置圆心位置、半径(米)、边框以及填充颜色。

### 示例代码如下：

```typescript
// 带边框的圆
let stroke:Stroke = new Stroke({
    strokeWidth: 12,
    color: '#f00',
    strokeStyle: SysEnum.StrokeStyle.SQUARE
});
this.circle = new Circle({
    center: new LatLng(39.915935, 116.402119),
    fillcolor: 'rgba(200, 120, 56, 0.5)',
    radius: 6000,
});
```

### 绘制棱柱

提供Prism类，实现棱柱的绘制。可以通过API设置底面坐标、高度、侧面颜色、顶面颜色、侧面纹理。

```typescript
let prism = new Prism({
  points: [new LatLng(30, 110), new LatLng(30, 110.02), new LatLng(29.985, 110.02),
      new LatLng(29.985, 110)],
  height: 600,
  topFaceColor: 'rgba(17, 29, 234,0.6)',
  sideFaceColor: 'rgba(17, 29, 234,1)',
})
this.mapController.addOverlay(prism);

let prism2 = new Prism({
    points: [new LatLng(30+0.05, 110), new LatLng(30+0.05, 110.02),
        new LatLng(29.985+0.05, 110)],
      height: 500,
      topFaceColor: 'rgba(255, 0, 0, 0.5)',
      sideFaceColor: 'rgba(255, 0, 0, 0.7)',
})
this.mapController.addOverlay(prism2);
```

### 绘制海量点

2.0.3版本起SDK支持海量点图层绘制，用于批量展现坐标点数据

### 添加海量点数据：

通过IMultiPointOption来设置海量点图层的属性，绘制的示例代码如下：

```typescript
let jsonFile = getContext().resourceManager.getRawFileContentSync("locations.json");
let str = buffer.from(jsonFile.buffer).toString()
const data :Record<string, number>[] = JSON.parse(str);
const datas = data.map(item=>new LatLng(item.lat,item.lng));
const multiPoint = new MultiPoint({
    multiPointItems: datas.map(item=> new MultiPointItem(item)),
    icon: new ImageEntity("rawfile://map_marker_red.png")
})
this.mapController?.addOverlay(multiPoint);
```
### 绘制动态轨迹

2.0.3 起支持动态轨迹绘制，开发者可以提供轨迹数据，来动态展示轨迹，支持监听轨迹绘制状态，具体配置可参考ITrackOption。

### 绘制2D动态轨迹

1、通过trackType来设置轨迹类型为TrackType.Track，即普通2D动态轨迹。

示例代码如下：

```typescript
this.track = new Track({
    points: trace, // 路线坐标点
    trackMove: true, 
    trackType: SysEnum.TrackType.Track
    opacity: 0.5,
    animationTime: 5000,
    traceAnimationListener: mTraceAnimationListener
})
this.mapController?.addOverlay(this.track);
```

2、设置动态轨迹监听回调。

示例代码如下：

```typescript
const mTraceAnimationListener:TraceAnimationListener = {
    /**
     * 轨迹动画更新进度回调
     * @param percent 轨迹动画更新进度，取值范围 [0, 100]（0 表示开始，100 表示结束）
     */
    onTraceAnimationUpdate:(percent: number) => {
    },
    /**
     * 轨迹动画当前位置更新回调
     * @param position 轨迹动画当前帧的位置坐标（经纬度信息）
     */
    onTraceUpdatePosition:(position: LatLng)=>{
    },
    /**
     * 轨迹动画结束回调
     * 当动画播放完成（包括正常结束、手动停止）时触发
     */
    onTraceAnimationFinish:() =>{
    }
}
```

3、渐变轨迹线

动态轨迹支持为每个轨迹点配置颜色来实现渐变轨迹效果。通过trackType为TrackType.TrackGradient并传入的gradientColors来开启，传入int类型十六进制或者rgb形式的颜色数组。

代码如下：

```typescript
const colors = [
    0xAA0000FF,0xAA00FF00,0xAAFF0000,
    0xAA0000FF,0xAA00FF00,0xAAFF0000,
    0xAA0000FF,0xAA00FF00,0xAAFF0000,
    0xAA0000FF,0xAA0000FF,0xAA00FF00,
    0xAAFF0000,
];
this.track = new Track({
    points: trace,
    trackMove: true,
    trackType: SysEnum.TrackType.TrackGradient,,
    gradientColors:colors,
    animationTime: 5000,
    traceAnimationListener: mTraceAnimationListener
})
```


### 绘制3D动态轨迹

1、通过设置trackType为TrackType.Surface绘制3D表面轨迹类型

```typescript
let trace = [
    new LatLng(40.055826, 116.307917), new LatLng(40.055916, 116.308455), new LatLng(40.055967, 116.308549),
    new LatLng(40.056014, 116.308574), new LatLng(40.056440, 116.308485), new LatLng(40.056816, 116.308352),
    new LatLng(40.057997, 116.307725), new LatLng(40.058022, 116.307693), new LatLng(40.058029, 116.307590),
    new LatLng(40.057913, 116.307119), new LatLng(40.057850, 116.306945), new LatLng(40.057756, 116.306915),
    new LatLng(40.057225, 116.307164), new LatLng(40.056134, 116.307546), new LatLng(40.055879, 116.307636),
    new LatLng(40.055826, 116.307697),
];
const heightArr: number[] = [
    100,200,100,
    300,100,100,
    100,50,100,
    600,123,56,
    800,345,1000,
    600,
];
const palettePng:ImageEntity = new ImageEntity("rawfile://track_palette.png");
this.track = new Track({
    points: trace,
    trackMove: true,
    palette:palettePng, //必传，设置3D轨迹调色板
    trackType: SysEnum.TrackType.Surface,
    heights: heightArr, //必传，3D轨迹高度数组，设置3D轨迹高度，长度必须和points一致
    animationTime: 5000,
    traceAnimationListener: mTraceAnimationListener
})
```


2、通过设置trackType为TrackType.Default3D绘制默认3D轨迹类型

```typescript
...
const projectionPalettePng:ImageEntity = new ImageEntity("rawfile://track_projection_palette.png");
this.track = new Track({
    points: trace,
    trackMove: true,
    palette:palettePng,
    paletteOpacity: 0.5,
    projectionPalette:projectionPalettePng, //底部阴影调色板，在trackType为SysEnum.TrackType.Default3D时必传
    trackType: SysEnum.TrackType.Default3D,
    heights: heightArr,
    animationTime: 5000,
})
this.mapController?.addOverlay(this.track);
```


### 路名绘制

#### 一、接口变更

新增路名绘制类TextPathMarker。

#### 设置路名文字:

```typescript
  /**
   * 设置路名
   * @param text 路名字符串
   */
  public setText(text: string): void
```

#### 设置文字的颜色

```typescript
/**
   * 设置文字颜色（ARGB 格式）
   * @param argb 颜色值（如 0xFF0000FF 表示蓝色）
   */
  public setTextColor(argb: number): void
```

#### 设置文字的大小

```typescript
/**
   * 设置文字大小
   * @param size 文字大小（单位：px）
   */
  public setTextSize(size: number): void 
```

#### 设置文字描边的颜色

```typescript
/**
   * 设置文字描边颜色
   * @param argb 描边颜色（ARGB 格式）
   */
  public setTextBorderColor(argb: number): void
```

#### 设置文字描边的宽度

```typescript
/**
   * 设置文字描边宽度
   * @param width 描边宽度（px）
   */
  public setTextBorderWidth(width: number): void
```

#### 设置字体格式

```typescript
/**
   * 设置字体格式
   * @param option Typeface 字体对象
   */
  public setTextFontOption(option: number): void 
```

#### 道路参数：

设置展示路名的道路

```typescript
 /**
   * 设置展示路名的道路坐标点（需至少 2 个点）
   * @param points 经纬度坐标列表
   */
  setPoints(points: Array<LatLng>): void 
```

注：路名绘制需要依赖Polyline先绘制出一条线路

```typescript
let trace = [
    new LatLng(39.97923, 116.357428),
    new LatLng(39.94923, 116.397428),
    new LatLng(39.97923, 116.437428)
];
let polyline = new Polyline(
{
  points: trace,
  width: 5,
});
this.mapController?.addOverlay(polyline);

let textPathMarker = new TextPathMarker({
    text: '自定义路线',
    textColor: 0xAA0000FF,
    textSize: 25,
    points: trace,
    //textBorderWidth: 10,
    //textBorderColor: 0xAA0000FF,
    //textFontOption: 1,
})
this.mapController?.addOverlay(textPathMarker);
```

### 路名绘制

通过Ground类，设置四至范围，纹理以及透明度，支持在底图上叠加地面覆盖物（自定义图片）。

#### 示例代码：

```typescript
// 添加地面覆盖物
const image:ImageEntity = new ImageEntity("rawfile://ground.png");
this.ground = new Ground({
    image: image,
    bounds: [new LatLng(35, 100), new LatLng(45, 120)],
    transparency: 0.8
});
this.ground.addEventListener(OverlayEvent.CLICK, () => {
    this.ground?.setBound(new LatLng(40, 100), new LatLng(50, 120));
    promptAction.showToast({
        message: "点击地面覆盖物",
        duration: 2000,
    });
});
```

### 地面覆盖物

从2.0.0版本开始，不再支持InfoWindow覆盖物类型，请使用PopView进行信息框开发。

#### PopView

[PopView](https://lbsyun.baidu.com/api/harmony?title=harmonynextsdk/guide/render-map/infowindow#PopView)可以通过设置[LableUI](https://lbsyun.baidu.com/api/harmony?title=harmonynextsdk/guide/render-map/infowindow#LableUI)文本UI，[TextStyle](https://lbsyun.baidu.com/api/harmony?title=harmonynextsdk/guide/render-map/infowindow#TextStyle)文本样式，[HorizontalLayout](https://lbsyun.baidu.com/api/harmony?title=harmonynextsdk/guide/render-map/infowindow#HorizontalLayout)水平布局，[VerticalLayout](https://lbsyun.baidu.com/api/harmony?title=harmonynextsdk/guide/render-map/infowindow#VerticalLayout)垂直布局，[ImageUI](https://lbsyun.baidu.com/api/harmony?title=harmonynextsdk/guide/render-map/infowindow#ImageUI)设置图像UI，来实现信息框覆盖物的创建。

[Marker](https://lbsyun.baidu.com/api/harmony?title=harmonynextsdk/guide/render-map/infowindow#Marker)的 icon图标通过[ImageEntity](https://lbsyun.baidu.com/api/harmony?title=harmonynextsdk/guide/render-map/infowindow#ImageEntity)对象设置,通过透明图标作为瞄点，来实现信息框。

```typescript
import {MapController,Marker,ImageEntity,SysEnum,LabelUI,CommonEvent,TextStyle,PopView} from '@bdmap/map';

mapController: MapController | null = null;
marker: Marker | null = null;
// transparent.png为透明图标
let image = new ImageEntity('rawfile://transparent.png');
this.marker = new Marker({
              position: new LatLng(39.904835, 116.403119),
              icon: image,
              located: SysEnum.Located.CENTER,
              isClickable: false
            });

/** PopView */
{
    let layout = new HorizontalLayout();
    layout.setBackground(new ImageEntity("rawfile://pop_bottom.png"),{
    /** 横向可缩放区域 [x1,x2] or [x1,x2,x3,x4] @since 1.2.0*/
    scaleX: [20,40,100,120],
    /** 纵向可缩放区域 [y1,y2] or [y1,y2,y3,y4]  @since 1.2.0*/
    scaleY: [40,80],
    /**「.9」的内容区域 [x1,x2,y1,y2]  @since 1.2.0*/
    fillArea: [20,120,20,80]
    })
    layout.setBackgroundColor('#ffff')
    layout.setGravity(SysEnum.Gravity.GRAVITY_LEFT);
    let img = new ImageUI();
    img.setDrawableResource(new ImageEntity('rawfile://bg.png'));
    img.setWidth(64);
    img.setHeight(64);
    layout.addView(img);
    let label = new LabelUI();
    label.setGravity(SysEnum.Gravity.GRAVITY_CENTER);
    let line1 = `时间段：${start} - ${endHHmm}`;
    let line2 = `from百度地图`;
    // 字符串中可以使用换行符
    label.setText(`${line1} \n ${line2}`);             
    label.setBackgroundColor('rgba(255,235,59,0.5)')
    label.setPadding(20, 0, 0, 0);
    label.setClickable(false);
    label.addEventListener(CommonEvent.CLICK,(e:EventUIBundle)=>{
    })
    let txtStyle =  new TextStyle();
    txtStyle.setTextColor('rgba(255,0,255,1)');
    txtStyle.setTextSize(28);
    txtStyle.setFontOption(SysEnum.FontOption.BOLD);
    label.setStyle(txtStyle);
    layout.addView(label);
    let popView = this.popView = new PopView();
    popView.setVisibility(SysEnum.Visibility.VISIBLE);
    popView.setView(layout);
    popView.setLocated(SysEnum.Located.CENTER);
    popView.addEventListener(CommonEvent.CLICK,(e:EventUIBundle)=>{
    })
    // 附加PopView
    this.marker?.setPopView(popView);
}
 this.mapController?.addOverlay(this.marker);
```

#### InfoWindow

InfoWindow 类可以通过设置content纹理资源、position位置点以及yOffset偏移值，实现信息框覆盖物的创建。

可通过ArkUI获取PixelMap，赋值给InfoWindow实现信息框。

```typescript
@Builder
function RandomBuilder(a:string,b:string) {
    Flex({ direction: FlexDirection.Column, justifyContent: FlexAlign.Center, alignItems: ItemAlign.Center }) {
        Text('Test menu item ' + a)
            .fontSize(20)
            .width(100)
            .height(50)
            .textAlign(TextAlign.Center)
        Divider().color('#00ff00').height(10)
        Text('Test menu item ' + b)
            .fontSize(20)
            .width(100)
            .height(50)
            .textAlign(TextAlign.Center)
    }
    .width(100)
    .height(100)
    .backgroundColor('#ff88')
    .borderRadius(10)
    .id("builder")
}
componentSnapshot.createFromBuilder(()=>{RandomBuilder.bind(this)('ONE','TWO')})
    .then((pixmap: image.PixelMap) => {
        let info = componentUtils.getRectangleById("builder")
        let infoWin = this.infoWin = new InfoWindow({
            anchorX: 0.5,
            anchorY: 0,
            content: new ImageEntity(pixmap,info.size.width,info.size.height)
        })
        infoWin.addEventListener(OverlayEvent.CLICK,()=>{
            promptAction.showToast({
                message: '信息框点击',
                duration: 2000,
            });
        });
        this.marker?.setInfoWindow(infoWin);
    }).catch((err:Error) => {
    console.log("error: " + err)
})
```

通过直接使用图片纹理的形式赋值给InfoWindow实现信息框。

```typescript
 let info2 = new InfoWindow({
    position: new LatLng(39.914835, 116.413119),
    content: new ImageEntity('rawfile://info.png'),
    isPerspective: false,
    yOffset: -49
});
info2.addEventListener(OverlayEvent.CLICK,()=>{
    promptAction.showToast({
        message: '信息框点击',
        duration: 2000,
    });
});
this.mapController?.addOverlay(info2);
```

### 信息框

提供Building类继承Prism类的方法，实现建筑物的绘制。可以通过 API 设置楼面坐标或者BuildingInfo对象、高度、侧面/顶面颜色、侧面/顶面纹理以及动画配置。

#### 示例代码

```typescript
let latlng = new LatLng(23.008468, 113.72953)
let search: BuildingSearch = BuildingSearch.newInstance();
search.requestBuilding({ latlng })
    .then((res: BuildingResult) => {
    if (!!res.buildingList) {
        res.buildingList.forEach(item => {
            if (item.geom) {
               this.appendBuilding(item)
            }
        })
    }
})
appendBuilding(item: BuildingInfo) {
    let build = new Building({
        buildingInfo: item,
        sideFaceColor: Color.Blue,
        topFaceColor: Color.Green,
        floorColor: Color.Yellow,
        floorHeight: (item.height ?? 0) - 10,
        isRoundedCorner: true,
        roundedCornerRadius: 2,
        buildingFloorAnimateType: FloorAnimateType.AnimateSlow
    })
    this.mapController.addOverlay(build);
}
```

### 建筑物

地图SDK支持3D模型绘制，用于在地图上展示3D模型，目前支持obj+mtl文件格式模型加载。（注意：模型中的图片必须支持透明Alpha通道）

#### 通过I3DModelOption来设置3D模型的属性。

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| modelPath | string | 模型文件沙盒路径（必填）。用于指定模型文件在资源中的位置。|
| modelName | string | 模型文件名（必填），用于在地图中唯一标识该模型。|
| position | LatLng | 模型地理坐标（必填），指定模型放置的经纬度位置。|
| bm3DModelType | BM3DModelType | 模型文件类型（默认：BM3DModelType.BM3DModelTypeObj）。支持：.obj（0）、.gltf（1）。|
| alwaysShow | boolean | 模型是否不被楼栋遮挡。true：始终显示在楼栋上层；false：被楼栋遮挡。|
| scale | number | 模型缩放比例（默认：1.0）。值越大模型越大，0 时不可见。|
| zoomFixed | boolean | 缩放比例是否不随地图缩放变化（默认：false）。true表示固定大小。|
| rotateX | number | 模型绕 X 轴旋转角度（默认：0.0）。取值范围 [0, 360]。|
| rotateY | number | 模型绕 Y 轴旋转角度（默认：0.0）。取值范围 [0, 360]。|
| rotateZ | number | 模型绕 Z 轴旋转角度（默认：0.0）。取值范围 [0, 360]。|
| offsetX | number | X 轴偏移像素（默认：0.0）。正值向右，负值向左。|
| offsetY | number | Y 轴偏移像素（默认：0.0）。正值向下，负值向上。|
| offsetZ | number | Z 轴偏移像素（默认：0.0）。影响模型在 3D 空间的前后层级。|
| animationIsEnable | boolean | 模型骨骼动画是否启用（默认：false）。仅 GLTF 模型支持。|
| animationRepeatCount | number | 动画重复执行次数（默认：0 表示无限循环）。|
| animationSpeed | number | 模型动画播放倍速（默认：1.0）。|
| animationIndex | number | 当前播放的动画索引（GLTF 模型可包含多帧动画）。|

### 示例代码

示例代码如下：

```typescript
const model = new Bd_3DModel({
    position: new LatLng(39.94923, 116.397428),
    modelPath: filePath,
    modelName: 'among_us',
    bm3DModelType: SysEnum.BM3DModelType.BM3DModelTypeObj,
    animationIsEnable: true,
    scale: 5
});
this.mapController?.addOverlay(model)
```

#### GLTF动画

其对应的配置参数如下：

```typescript
const model = new Bd_3DModel({
    position: new LatLng(39.94923, 116.397428),
    modelPath: filePath,
    modelName: 'scenes',
    bm3DModelType: SysEnum.BM3DModelType.BM3DModelTypeglTF, //动画类型
    animationIsEnable: true,
    scale: 10
});
this.mapController?.addOverlay(model);
```

绘对应展示效果如下：

抱歉，您的浏览器不支持video标签

### 绘制3D模型

覆盖物图层是指可以管理覆盖物要素数据的图层

#### 默认覆盖物图层

地图创建后，默认会生成一个覆盖物图层，此覆盖物图层会跟随地图实例进行销毁。

##### 获取默认覆盖物图层

```typescript
let layer = this.mapController.getOverlayLayer();
```

##### 默认覆盖物图层上增删数据

```typescript
// 添加地图覆盖物
this.mapController.addOverlay(overlay: Overlay);

// 移除地图覆盖物
this.mapController.removeOverlay(overlay: Overlay);

// 按类别移除地图覆盖物
this.mapController.removeOverlays(type?: SysEnum.OverlayType);
```

#### 自定义覆盖物图层

用户通过API创建覆盖物图层，实现数据分类管理。

##### 1.创建或移除图层

```typescript
// 创建覆盖物图层
let selfLayer = this.mapController.createOverlayLayer();

// 移除覆盖物图层
this.mapController.removeOverlayLayer(selfLayer);
```

##### 2.添加或移除覆盖物

```typescript
// 添加地图覆盖物
selfLayer.addOverlay(overlay: Overlay);

// 移除地图覆盖物
selfLayer.removeOverlay(overlay: Overlay);

// 按类别移除地图覆盖物
selfLayer.removeOverlays(type?: SysEnum.OverlayType);
```

#### 其他

##### 1.获取所有覆盖物图层

```typescript
let result = this.mapController.getLayerByTag(SysEnum.LayerTag.OVERLAY);
if (result) {
    if (Array.isArray(result)) {
        // 包含默认覆盖物图层以及自定义覆盖物图层，索引为0的图层即为默认覆盖物图层。
        let layer = result as Array<OverlayLayer>;
    } else {
        // 只有一个默认覆盖物图层
        let layers = result as OverlayLayer;
    }
}
```

##### 2.监听所有图层覆盖物事件

```typescript
this.mapController.addOverlayEventListener(
    SysEnum.EOverLayTypeName.MARKER,
    OverlayEvent.CLICK,
    (bundle: EventOverlayBundle) => {
        let overlays = bundle.target as Array<Overlay>;
        if (overlays && overlays.length > 0) {
            overlays.forEach(item => {
                if (item instanceof Marker) {
                    promptAction.showToast({
                        message: 'Marker被点击',
                        duration: 2000,
                    });
                }
            });
        }
    }
);
```

### 瓦片图层

通过配置符合百度网格瓦片标准的数据源，加载到基础地图上进行显示。

#### 定义数据源

```typescript
/**
 * 定义瓦片图的在线Provider，并实现相关接口
 * MAX_LEVEL、MIN_LEVEL 表示地图显示瓦片图的最大、最小级别
 * urlString 表示在线瓦片图的URL地址
 */
class OnlineTileProvider extends UrlTileProvider{
  override getMaxDisLevel() {
    return 16;
  }
  override getMinDisLevel() {
    return 6;
  }
  override getTileUrl() {
    return "http://online1.map.bdimg.com/tile/?qt=vtile&x={x}&y={y}&z={z}&styles=pl&scaler=1&udt=20190528";
  }
}
```

#### 加载到地图

可以设置显示层级范围、地理范围和显示隐藏等。

```typescript
// 2.0.0版之前，通过外部调用实例化
this.imageTileLayer = new ImageTileLayer(new OnlineTileProvider());

// 2.0.0版本及之后，通过内部实例化
this.imageTileLayer = ImageTileLayer.createWithMapControl(this.mapController,new OnlineTileProvider()) as ImageTileLayer;

this.imageTileLayer?.setDisplayLevel(8,21);
this.imageTileLayer?.setSourceRegion(new Bounds(new LatLng(30, 100),new LatLng(60, 120)));

// 2.0.0版之前需要手动添加，2.0.0版本及之后不需要手动添加
this.mapController?.addTileLayer(this.imageTileLayer);

// 显示隐藏控制
this.imageTileLayer?.setVisible(true);
this.imageTileLayer?.setVisible(false);
```

#### 从地图移除

移除瓦片图层，并销毁

```typescript
this.mapController?.removeTileLayer(this.imageTileLayer);
this.imageTileLayer = undefined;
```

<a id="ref-map-heatmap-3d"></a>

### 动态热力图

地图SDK支持动态热力图功能，支持以3D的形式表示数据的密度和分布情况。

#### 添加热力图图层步骤：

##### 1.准备经纬度分布数据集

```typescript
const data :Record<string, number>[] = [
    {"lng": 116.895579, "lat": 24.306521},
    {"lng": 113.951068, "lat": 22.772504},
    // ... 更多数据
]
```

##### 2.设置热力图属性

```typescript
// 获取热力图数据集
 const heatMapDatas = data.map(item=>{
    return new WeightedLatLng(new LatLng(item.lat,item.lng), 1)
})

//设置渐变色
const gradinet = new Gradient([
    'rgba(0,0,200,1)', 'rgba(0,225,0,1)', 'rgba(255,0,0,1)'
  ], [0.3, 0.7, 1.0]);

this.heatMap = new HeatMapBuilder()
              .setDatas(heatMapDatas)
              .gradientValue(gradinet)
              .isRadiusMeterValue(true)
              .radiusMeterValue(100)
              .opacityValue(1.0)
              .maxIntensityValue(1)
              .frameAnimationValue(new HeatMapAnimation(true, 2000, AnimationType.OutQuad))
              .build();
```

##### 3.操作热力图

```typescript
// 添加热力图
this.mapController.addHeatMap(this.heatMap);

// 开启热力图帧动画
this.mapController.startHeatMapFrameAnimation();

// 停止热力图帧动画
this.mapController.stopHeatMapFrameAnimation();

// 调整热力图帧数（例如设置为第2帧）
this.mapController?.setHeatMapFrameAnimationIndex(1);
```

<a id="ref-map-heatmap-hexagon"></a>

### 动态热力图

在地图上绘制2D蜂窝热力图，配置项参考HexagonMapBuilder类。

#### 示例代码：

```typescript
const data = [
{"lng":116.895579,"lat":24.306521},
{"lng":113.951068,"lat":22.772504},
// ...
{"lng":110.00006,"lat":40.603564},
{"lng":111.846788,"lat":21.897821}
]

const datas = data.map(item=>new WeightedLatLng(new LatLng(item.lat,item.lng)),1);

this.hexagonMap = new HexagonMapBuilder()
                  .setData(datas)
                  .radiusValue(radius)
                  .gapValue(gap)
                  .minIntensityValue(minIntensity)
                  .maxIntensityValue(maxIntensity)
                  .minShowLevelValue(minShowLevel)
                  .maxShowLevelValue(maxShowLevel)
                  .setHexagonType(hexagonType)
                  .setGradient(gradient)
                  .opacityValue(opacity)
                  .build();

this.mapController.addHexagonMap(this.hexagonMap);
```

### 2D蜂窝热力图

开发者可通过调用 `mapController.setLocationInfo` 方法对定位图层进行定位数据、展示配置等控制。

#### 核心参数：

- **ILocation (定位点数据)**: 包括 `latlng` (坐标)、`direction` (方向角度)、`radius` (精度)、`speed` (速度)等。
- **ILocationConfig (展示配置)**: 包括 `locationMode` (显示方式)、`enableDirection` (是否显示方向)、`customMarker` (自定义图标)、`accuracyCircleFillColor` (精度圈颜色)等。

#### 示例代码：

#### 1.显示定位

```typescript
MapComponent({ onReady: async (err, mapController) => {
    if (!err) {
        this.mapController = mapController;
        let myLocation: ILocation = {
            latlng: new LatLng(39.907916, 116.408599),
            direction: 90,
            radius: 1000
        }
        this.mapController?.setLocationInfo(myLocation, {
          locationMode: SysEnum.LocationMode.NORMAL
        });
    }
}})
```

##### 2.定位模式

地图SDK支持三种定位模式：
- `NORMAL`: 普通态
- `FOLLOWING`: 跟随态
- `COMPASS`: 罗盘态

```typescript
this.mapController?.setLocationConfig({
  locationMode: SysEnum.LocationMode.FOLLOWING
})
```

##### 3.自定义定位图标

```typescript
let config: ILocationConfig = {
    isEnableCustom: true,
    arrow: endIcon, // 箭头图标
    customMarker: userIcon, // 定位图标
    markerSize: 0.2,
    isNeedAnimation: true // 开启呼吸动画
}
this.mapController.setLocationConfig(config)
```

<a id="ref-map-compass-layer"></a>

### 方向图层

可通过调用 `CompassLayer` 类方法或者属性进行定位位置、显示隐藏等控制，通过点击图标可重置地图方向。

#### 示例代码：

```typescript
MapComponent({ onReady: async (err, mapController) => {
    if (!err) {
        // 获取地图的控制器类，用来操作地图
        this.mapController = mapController;
        this.compass = this.mapController.getLayerByTag(SysEnum.LayerTag.COMPASS) as CompassLayer;
        this.compass.x = 64;
        this.compass.y = 64;
    }
}, mapOptions: new MapOptions(null)}).width('100%').height('100%')
```

## 3. 检索能力（模块：search）

> 模块：`@bdmap/search`　docs：`api/modules/search.md`　常用检索词：PoiSearch / GeoCoder / AoiSearch / SuggestionSearch / BusLineSearch / WeatherSearch / DistrictSearch / BuildingSearch

### POI检索

HarmonyOS地图SDK提供多种类型的POI（兴趣点）检索功能。

#### 1.城市内检索

```typescript
let search: PoiSearch = PoiSearch.newInstance();
let optionParams: PoiCitySearchOptionParams = {
  city: '北京市',
  keyword: '美食'
}
let option = new PoiCitySearchOption(optionParams)
search.searchInCity(option).then((res: PoiResult) => {
    // 处理结果
})
```

#### 2.周边检索

```typescript
let search: PoiSearch = PoiSearch.newInstance();
let opParams: PoiNearbySearchOptionParams = {
  keyword: "美食$酒店",
  location: new LatLng(39.915, 116.404),
  radius: 1000
}
let option = new PoiNearbySearchOption(opParams)
search.searchNearby(option).then((res: PoiResult) => {
    // 处理结果
})
```

#### 3.区域检索（矩形区域）

```typescript
let search: PoiSearch = PoiSearch.newInstance();
let southWest = new LatLng(40.049, 116.279)
let northEast = new LatLng(40.056, 116.308)
let optionParams: PoiBoundSearchOptionParams = {
  bound: new LatLngBounds(southWest, northEast),
  keyword: '美食'
}
let option = new PoiBoundSearchOption(optionParams)
search.searchInBound(option).then((res: PoiResult) => {
    // 处理结果
})
```

#### 4.其他检索

- **POI详情检索**: `search.searchPoiDetail({ uids: uid })`
- **室内检索**: `search.searchPoiIndoor({ bid: bid, wd: wd, floor: floor })`

### 地理编码

地理编码是地址信息和地理坐标之间的相互转换。

#### 1.正地理编码（地址 -> 坐标）

```typescript
geoSearch() {
    let search: GeoCoder = GeoCoder.newInstance();
    let option: GeoCodeOption = new GeoCodeOption('北京市', '海淀区上地十街10号')
    search.geocode(option).then((res: GeoCodeResult) => {
         // 处理结果 res.location
    })
}
```

#### 2.逆地理编码（坐标 -> 坐标）

```typescript
reGeoSearch() {
    let search: GeoCoder = GeoCoder.newInstance();
    let opParams: ReverseGeoCodeOptionParams = {
      location: new LatLng(39.915, 116.404)
    }
    let option = new ReverseGeoCodeOption(opParams)
    search.reverseGeoCode(option).then((res: ReverseGeoCodeResult) => {
        // 处理结果 res.address
    })
}
```

### AOI检索

根据用户输入的指定地点经纬度，返回对应地点AOI面的边界信息。
*使用说明：该服务为高级权限，需申请权限后才可以使用。*

#### 实现步骤：

```typescript
AoiSearch.newInstance().requestAoi({
  latLngList: [new LatLng(40.070754, 116.324175)]
})
.then((res: AoiResult) => {
    // TODO: 处理返回的边界信息
})
```

<a id="ref-search-suggestion"></a>

### 地点输入提示检索（Sug检索）

Sug检索是指根据关键词查询在线建议词，帮助开发者实现关键词快速定位。

#### Sug检索与POI检索的区别：
- **Sug检索**: 根据部分关键字匹配出可能的完整关键字名称。
- **POI检索**: 根据关键字检索符合的POI具体信息。

#### 示例代码：

```typescript
let sugSearch = SuggestionSearch.newInstance();
let option: SuggestionSearchOption = {
      city: '北京市',
      keyword: '肯德基'
}

sugSearch.requestSuggestion(option).then((res: SuggestionResult) => {
    // 处理返回的热词建议列表
})
```

### 公交信息检索

公交路线信息检索分为两步：首先通过 POI 检索获取公交/地铁线路的 UID，然后使用 `BusLineSearch` 获取详细信息。

#### 1.获取公交路线 UID

```typescript
let search: PoiSearch = PoiSearch.newInstance();
let optionParams: PoiCitySearchOptionParams = {
  city: "北京",
  keyword: "963",
  scope: 2
}
search.searchInCity(optionParams).then((res: PoiResult) => {
    // 遍历结果，寻找 POITYPE.BUS_LINE 或 POITYPE.SUBWAY_LINE
    // 获取对应的 uid
})
```

#### 2.检索公交线路详细信息

```typescript
let busLineSearch: BusLineSearch = BusLineSearch.newInstance()
busLineSearch.searchBusLine({
  uid: busLineId,
  city: '北京'
})
.then((res: BusLineResult) => {
    // 处理公交路线详情（站点、票价等）
})
```

### 天气服务

提供国内及海外的天气查询服务。

#### 服务内容：
- **基础服务**: 通过行政区划代码查询实时天气及未来5天预报。
- **高级权限**: 通过经纬度查询实时天气、未来7天预报、逐小时预报、空气质量、气象预警等。

#### 实现步骤：

```typescript
let search = WeatherSearch.newInstance()
let option: WeatherSearchOption = {
  districtID: '110108' // 行政区划代码
}

search.request(option).then((res: WeatherResult) => {
    // 处理天气结果
})
```

### 推荐上车点

基于用户定位，推送周边合理的上车位置，降低接驾时间。

#### 实现步骤：

```typescript
search.requestRecommendStop({
  location: new LatLng(39.915, 116.404)
})
.then((res: RecommendStopResult) => {
    if (res.error === ERRORNO.NO_ERROR && res.recommendStopInfoList) {
      res.recommendStopInfoList.forEach(info => {
        let stopLocation = new LatLng(info.bd09ll_y, info.bd09ll_x);
        // 在地图上添加推荐上车点的 Marker
        let marker = new Marker({ position: stopLocation, ... });
        this.map?.addOverlay(marker);
      });
    }
})
```

### 检索行政区边界数据

根据省、市、县（区）级行政区划名称，返回所查询行政区划边界的详细坐标信息。

#### 示例代码：

```typescript
let search: DistrictSearch = DistrictSearch.newInstance();
search.searchDistrict({
  cityName: '北京市',
  districtName: '海淀区'
})
.then((res: DistrictResult) => {
    // 处理行政区边界数据 res.polylines
})
```

### 地图建筑物检索

通过该接口可以检索出地图上的3D楼块数据。
*使用说明：该服务为高级权限，需申请权限后才可以使用。*

#### 实现步骤：

```typescript
let search: BuildingSearch = BuildingSearch.newInstance();
search.requestBuilding({
    latlng: new LatLng(39.915, 116.404)
})
.then((res: BuildingResult) => {
    // 处理 3D 楼块数据
})
```

## 4. 路线规划（模块：search + walkridecommon 或组合包）

> docs：`api/modules/search.md`、`api/modules/walkridecommon.md`　常用检索词：RoutePlanSearch / drivingSearch / walkingSearch / bikingSearch / transitSearch / masstransitSearch

### 驾车路线规划

根据起终点获取驾车路线规划数据，并可以通过添加 `Polyline` 绘制出驾车路线。

#### 示例代码：

```typescript
let lineTexture = new ImageEntity('rawfile://Icon_road_blue_arrow.png');

let option: DrivingRoutePlanOption = {
  mFrom: PlanNode.withLocation(fromLatLng),
  mTo: PlanNode.withLocation(toLatLng)
}

RoutePlanSearch.newInstance().drivingSearch(option).then((res: DrivingRouteResult) => {
    if (!res.routeLines) return;
    
    let resultLine: Array<LatLng> = [];
    let line = res.routeLines[0];
    line.steps.forEach(step => {
      step.pathList.forEach(element => {
        resultLine.push(element);
      });
    });

    let polyline = new Polyline({
      points: resultLine,
      fillcolor: '#6af',
      width: 10,
      join: SysEnum.LineJoinType.ROUND,
      cap: SysEnum.LineCapType.ROUND,
      textures:[lineTexture],
      zIndex: 1
    });
    this.map?.addOverlay(polyline);
})
```

### 骑行路线规划

根据起终点获取骑行路线规划数据。

#### 示例代码：

```typescript
let lineTexture = new ImageEntity('rawfile://Icon_road_blue_arrow.png');

let option: BikingRoutePlanOption = {
  from: PlanNode.withLocation(fromLatLng),
  to: PlanNode.withLocation(toLatLng)
}

RoutePlanSearch.newInstance().bikingSearch(option).then((res: BikingRouteResult) => {
    if (!res.routeLines) return;
    
    let resultLine: Array<LatLng> = [];
    let steps = res.routeLines[0].steps;
    steps.forEach(step => {
      // parseStrPathToLLArray 是一个工具函数，将路径字符串转换为经纬度数组
      let line = parseStrPathToLLArray(step.pathString);
      resultLine = resultLine.concat(line);
    });

    let polyline = new Polyline({
      points: resultLine,
      fillcolor: '#6af',
      width: 10,
      textures:[lineTexture],
      zIndex: 1
    });
    this.mapController?.addOverlay(polyline);
})
```

### 公交路线规划

支持市内公交和跨城公交路线规划。

#### 1.市内公交路线规划

```typescript
let lineTexture = new ImageEntity('rawfile://Icon_road_blue_arrow.png');

let option: TransitRoutePlanOption = {
  from: PlanNode.withLocation(fromLatLng),
  to: PlanNode.withLocation(toLatLng)
}

RoutePlanSearch.newInstance().transitSearch(option).then((res: TransitRouteResult) => {
    if (!res.routeLines) return;
    
    let resultLine: Array<LatLng> = [];
    let steps = res.routeLines[0].steps;
    steps.forEach(step => {
      let llAry = parseGeoStr2LLArray(step.pathString);
      resultLine = resultLine.concat(llAry);
    });

    let polyline = new Polyline({
      points: resultLine,
      fillcolor: '#a6f',
      width: 10,
      textures:[lineTexture],
      zIndex: 1
    });
    this.mapController?.addOverlay(polyline);
})
```

#### 2.跨城公交路线规划

```typescript
const massOpt: MassTransitRoutePlanOption = { from, to }
RoutePlanSearch.newInstance().masstransitSearch(massOpt).then((res: MassTransitRouteResult) => {
    // 处理跨城公交结果，逻辑类似市内公交，需遍历多层 steps
})
```

### 步行路线规划

根据起终点获取步行路线规划数据。

#### 示例代码：

```typescript
let lineTexture = new ImageEntity('rawfile://Icon_road_blue_arrow.png');

let option: WalkingRoutePlanOption = {
  from: PlanNode.withLocation(fromLatLng),
  to: PlanNode.withLocation(toLatLng)
}

RoutePlanSearch.newInstance().walkingSearch(option).then((res: WalkingRouteResult) => {
    if (!res.routeLines) return;
    
    let resultLine: Array<LatLng> = [];
    let steps = res.routeLines[0].steps;
    steps.forEach(step => {
      let llAry = parseGeoStr2LLArray(step.pathString);
      resultLine = resultLine.concat(llAry);
    });

    let polyline = new Polyline({
      points: resultLine,
      fillcolor: '#6af',
      width: 10,
      textures:[lineTexture],
      zIndex: 1
    });
    this.map?.addOverlay(polyline);
})
```

## 5. 工具类能力与其他（模块：util / map / search）

> docs：`api/modules/util.md`、`api/modules/base.md`　常用检索词：DistanceUtil / AreaUtil / SpatialRelationUtil / NativeMethods / FavoriteManager / ShareUrlSearch

### 距离和面积计算

提供地图上两点间距离及区域面积的计算工具。

#### 1.两点距离计算

```typescript
import { DistanceUtil } from '@bdmap/util';
import { LatLng } from '@bdmap/base';

let p1LL: LatLng = new LatLng(39.9003, 116.3282);
let p2LL: LatLng = new LatLng(39.8707, 116.3859);
let distance: number = DistanceUtil.getDistance(p1LL, p2LL); // 单位：米
```

### 2.矩形面积计算

```typescript
import { AreaUtil } from '@bdmap/util';

let northeast: LatLng = new LatLng(40.117, 116.452);
let southwest: LatLng = new LatLng(39.615, 116.102);
let area: number = AreaUtil.calculateArea(northeast, southwest); // 单位：平方米
```

### 点和其他图形的位置关系

提供判断点与圆、多边形及折线位置关系的工具。

#### 1.点与圆的位置关系

```typescript
import { SpatialRelationUtil } from '@bdmap/util';

let center = new LatLng(39.915, 116.402);
let radius = 1000;
let mPoint = new LatLng(40.915, 116.402);
let isContained: boolean = SpatialRelationUtil.isCircleContainsPoint(center, radius, mPoint);
```

### 2.点与多边形的位置关系

```typescript
let mPoints: Array<LatLng> = [/* 多边形顶点列表 */];
let point: LatLng = new LatLng(40.915, 116.402);
let isContained: boolean = SpatialRelationUtil.isPolygonContainsPoint(mPoints, point);
```

### 3.点与折线的位置关系（获取线上最近点）

```typescript
let mPoints: Array<LatLng> = [/* 折线顶点列表 */];
let point: LatLng = new LatLng(40.915, 116.402);
let nearestPoint: LatLng | null = SpatialRelationUtil.getNearestPointFromLine(mPoints, point);
```

### 坐标转换

提供不同坐标系（WGS84、GCJ02、BD09）之间的转换方法。

#### 1.坐标转换方法

```typescript
import { NativeMethods } from '@bdmap/base';

// WGS84 转 BD09LL
let wgsll: LatLng = new LatLng(39.9, 116.4);
let bdll: LatLng | null = NativeMethods.wgsll2bdll(wgsll);

// GCJ02 转 BD09LL
let gcjll: LatLng = new LatLng(39.9, 116.4);
let bdll2: LatLng | null = NativeMethods.gcjll2bdll(gcjll);

// 百度墨卡托 (BD09MC) 转 百度经纬度 (BD09LL)
let mc: Point = new Point(x, y);
let bdll3: LatLng | null = NativeMethods.mc2ll(mc);
```

### 2.坐标系说明
- **WGS84**：GPS全球卫星定位系统使用的坐标系。
- **GCJ02**：国测局制订的加密坐标系统。
- **BD09**：百度坐标系，在 GCJ02 基础上再次加密。BD09LL 为经纬度坐标，BD09MC 为墨卡托米制坐标。
- **SDK支持**：鸿蒙地图 SDK 支持 BD09 和 GCJ02 两种坐标系。



### 调起百度地图功能介绍

鸿蒙版百度地图SDK提供简单的接口用来调起百度地图客户端（Native）来实现复杂的业务逻辑。支持的调起类型有：

- **主图**
- **标注**
- **反GEO**
- **POI检索**（POI详情检索、POI周边列表检索）
- **两框**
- **路线规划**（步行路线规划、骑行路线规划）
- **导航**

当手机中安装了百度地图客户端APP（版本号为1.0.0以上）时，开发者可以通过 `BaiduMapRoutePlan`、`BaiduMapPoiSearch`、`BaiduMapNavigation` 等类中的相关方法设置调起百度地图APP。如果未传入的坐标类型，则使用百度地图SDK的全局坐标类型。

**注**：通用参数和接口参数参考接口说明中鸿蒙端参数说明填写（[https://lbs.baidu.com/faq/api?title=webapi/uri/harmony](https://lbsyun.baidu.com/faq/api?title=webapi/uri/harmony)）

---

#### 调起百度地图主图功能（首页）

```typescript
import { CoordType } from '@bdmap/base';
import { BaiduMapRoutePlan, HomePageParamModel } from '@bdmap/util';

opnelink() {
    let context: common.UIAbilityContext = getContext(this) as common.UIAbilityContext;
    let homeParam: HomePageParamModel = new HomePageParamModel()
        .setBounds('915291, 403857, 056858, 308194')
        .setCoord_type(CoordType.BD09LL);
    try {
        BaiduMapRoutePlan.openBaiduMapHomePage(homeParam, context);
    } catch (e) {
        console.log('error:', JSON.stringify(e));
    }
}
```

#### 调起百度地图标注页功能

```typescript
import { BaiduMapRoutePlan, MarkerPageParamModel, SrcTypeEnum } from '@bdmap/util';

opnelink() {
    let context: common.UIAbilityContext = getContext(this) as common.UIAbilityContext;
    let markerParam: MarkerPageParamModel = new MarkerPageParamModel()
        .setTitle('我的位置')
        .setContent('天安门')
        .setLocation('39.915291,116.403857')
        .setSrc(SrcTypeEnum.PUSH);
    try {
        BaiduMapRoutePlan.openBaiduMapMarkerPage(markerParam, context);
    } catch (e) {
        console.log('error:', JSON.stringify(e));
    }
}
```

#### 调起百度地图反GEO功能

```typescript
import { BaiduMapRoutePlan, GeoCoderPageParamModel, SrcTypeEnum } from '@bdmap/util';

opnelink() {
    let context: common.UIAbilityContext = getContext(this) as common.UIAbilityContext;
    let geoParam: GeoCoderPageParamModel = new GeoCoderPageParamModel()
        .setAddress('天安门')
        .setSrc(SrcTypeEnum.PUSH);
    try {
        BaiduMapRoutePlan.openBaiduMapGeoCoderPage(geoParam, context);
    } catch (e) {
        console.log('error:', JSON.stringify(e));
    }
}
```

#### 调起百度地图POI详情页功能

```typescript
import { BaiduMapPoiSearch, PoiDetailPageParamModel } from '@bdmap/util';

opnelink() {
    let context: common.UIAbilityContext = getContext(this) as common.UIAbilityContext;
    let poiParam: PoiDetailPageParamModel = new PoiDetailPageParamModel()
        .setUid('8d96925c6ccf855cc1f1cf38');
    try {
        BaiduMapPoiSearch.openBaiduMapPoiDetialsPage(poiParam, context);
    } catch (e) {
        console.log('error:', JSON.stringify(e));
    }
}
```

#### 调起百度地图POI列表页功能

```typescript
import { BaiduMapPoiSearch, PoiSearchPageParamModel } from '@bdmap/util';

opnelink() {
    let context: common.UIAbilityContext = getContext(this) as common.UIAbilityContext;
    let poiLParam: PoiSearchPageParamModel = new PoiSearchPageParamModel()
        .setQuery('学校')
        .setLocation('39.989813,116.314094')
        .setRadius('1000');
    try {
        BaiduMapPoiSearch.openBaiduMapPoiNearbySearch(poiLParam, context);
    } catch (e) {
        console.log('error:', JSON.stringify(e));
    }
}
```

#### 调起百度地图两框页功能

```typescript
import { BaiduMapRoutePlan, RoutePageParamModel, RoutePageTypeEnum, IsTrueEnum } from '@bdmap/util';

opnelink() {
    let context: common.UIAbilityContext = getContext(this) as common.UIAbilityContext;
    let routeParam: RoutePageParamModel = new RoutePageParamModel()
        .setType(RoutePageTypeEnum.WALK)
        .setSrc(RoutePageTypeEnum.WALK)
        .setPopRoot(IsTrueEnum.NO)
        .setNeedLocation(IsTrueEnum.YES);
    try {
        BaiduMapRoutePlan.openBaiduMapRoutePage(routeParam, context);
    } catch (e) {
        console.log('error:', JSON.stringify(e));
    }
}
```

#### 调起百度地图路线页功能

```typescript
import {
    BaiduMapRoutePlan,
    DirectionPageParamModel,
    IsTrueEnum,
    SrcTypeEnum,
    TravelMethodEnum,
} from '@bdmap/util';

opnelink() {
    let context: common.UIAbilityContext = getContext(this) as common.UIAbilityContext;
    let dirParam: DirectionPageParamModel = new DirectionPageParamModel()
        .setPageflag('4')
        .setPopRoot(IsTrueEnum.NO)
        .setSrc(SrcTypeEnum.DUHELPER)
        .setOrigin('故宫')
        .setOriginName('故宫')
        .setDestination('天安门')
        .setDestName('天安门')
        .setMode(TravelMethodEnum.WALKING);
    try {
        BaiduMapRoutePlan.openBaiduMapDirectionPage(dirParam, context);
    } catch (e) {
        console.log('error:', JSON.stringify(e));
    }
}
```

#### 调起百度地图导航页功能

```typescript
import { BaiduMapNavigation, NaviPageParamModel } from '@bdmap/util';

opnelink() {
    let context: common.UIAbilityContext = getContext(this) as common.UIAbilityContext;
    let naviParam: NaviPageParamModel = new NaviPageParamModel()
        .setLocation('22.615108,114.035529')
        .setUid('6f6241e3c05ab1a093114c5e');
    try {
        BaiduMapNavigation.openBaiduMapNavi(naviParam, context);
    } catch (e) {
        console.log('error:', JSON.stringify(e));
    }
}
```

### 地图收藏夹

提供对收藏点（POI）的增删改查管理功能。

#### 1.初始化管理器

```typescript
import { FavoriteManager, FavoritePoiInfo } from "@bdmap/map";

// 获取单例实例
let favoriteMgr = FavoriteManager.getInstance();

// 销毁管理器，释放资源
// favoriteMgr.destroy();
```

#### 2.添加收藏点

```typescript
const poiInfo: FavoritePoiInfo = {
    id: "",                    // 新增时传空，成功后自动回填
    poiName: "我的家",         // 收藏点名称
    pt: new LatLng(39.915, 116.404),
    timeStamp: 0
};
const result: number = favoriteMgr.add(poiInfo); // 1 为成功
```

#### 3.管理接口
- **查询所有**：`favoriteMgr.getAllFavPois()` 返回 `Array<FavoritePoiInfo>`。
- **查询单个**：`favoriteMgr.getFavPoi(id)`。
- **删除**：`favoriteMgr.deleteFavPoi(id)`。
- **清空**：`favoriteMgr.clearAllFavPois()`。
- **更新**：`favoriteMgr.updateFavPoi(id, info)`。

### 位置短地址分享

通过生成短链接分享 POI 详情、位置坐标或路线规划结果。

#### 1.初始化

```typescript
import { ShareUrlSearch, ShareUrlResult } from "@bdmap/map";

const shareUrlSearch = ShareUrlSearch.newInstance();
// shareUrlSearch.destroy(); // 销毁实例
```

#### 2.分享类型
- **POI详情分享**：
  ```typescript
  const result = await shareUrlSearch.requestPoiDetailShareUrl({ uid: "POI_UID" });
  if (result.error === 0) console.log(result.url);
  ```
- **位置坐标分享**：
  ```typescript
  const result = await shareUrlSearch.requestLocationShareUrl({
      location: new LatLng(39.9, 116.4),
      name: "百度大厦",
      snippet: "北京市海淀区上地十街10号"
  });
  ```
- **路线分享**：支持驾车、步行、骑行、公交。
  ```typescript
  const result = await shareUrlSearch.requestRouteShareUrl({
      from: fromNode,
      to: toNode,
      routeShareMode: RouteShareMode.CAR_ROUTE_SHARE_MODE
  });
  ```
