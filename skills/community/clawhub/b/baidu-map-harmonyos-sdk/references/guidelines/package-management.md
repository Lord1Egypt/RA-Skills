## 鸿蒙百度地图 SDK 包管理规范

本文件规定了在 HarmonyOS NEXT 项目中引入百度地图 SDK 时，组合包与独立包的选择和互斥规则。

### 1. 包分类

百度地图鸿蒙 SDK 发布为**组合包**和**独立包**两种形式。

#### 1.1 组合包

组合包是多个独立包的集合，安装后即包含对应的全部独立包能力，使用时通过组合包包名引入。

| 组合包 | 包含的独立包能力 | 说明 |
| --- | --- | --- |
| `@bdmap/map_walkride_search` | `@bdmap/base`、`@bdmap/map`、`@bdmap/search`、`@bdmap/util` | 地图 + 步行/骑行路线 + 检索组合包 |
| `@bdmap/navi_map` | `@bdmap/base`、`@bdmap/map`、`@bdmap/search`、`@bdmap/util` | 导航 + 地图组合包 |

#### 1.2 独立包

独立包可按需单独安装，适用于只需要部分能力的场景。

| 独立包 | 能力 |
| --- | --- |
| `@bdmap/base` | 基础能力（坐标类型、AK 鉴权等） |
| `@bdmap/map` | 地图组件、控制器、覆盖物、图层等 |
| `@bdmap/search` | POI/AOI/行政区/天气/路线规划等检索能力 |
| `@bdmap/util` | 距离/面积计算、空间关系判断、坐标转换等工具 |
| `@bdmap/locsdk` | 定位 SDK（前台/后台定位、地址/POI 获取） |

> **注意**：`@bdmap/locsdk` 是独立的定位能力包，不属于任何组合包，可与组合包或独立包搭配使用。

### 2. 互斥规则（强制）

**组合包与独立包不允许混用。** 组合包内部已包含对应独立包的全部能力，如果同时安装会导致依赖冲突或运行时异常。

#### 2.1 禁止行为

- **禁止**在已安装组合包 `@bdmap/map_walkride_search` 的项目中，再单独安装 `@bdmap/base`、`@bdmap/map`、`@bdmap/search`、`@bdmap/util` 中的任何一个。
- **禁止**在已安装组合包 `@bdmap/navi_map` 的项目中，再单独安装 `@bdmap/base`、`@bdmap/map`、`@bdmap/search`、`@bdmap/util` 中的任何一个。
- **禁止**同时安装两个组合包（如同时安装 `@bdmap/map_walkride_search` 和 `@bdmap/navi_map`）。

#### 2.2 允许行为

- 使用组合包时，可以额外安装 `@bdmap/locsdk`（因为定位包不包含在组合包中）。
- 仅使用独立包时，可以自由组合安装多个独立包。

### 3. import 引用差异

使用组合包和独立包时，代码中的 import 路径不同：

```ts
// ✅ 使用组合包 @bdmap/map_walkride_search 时：
import { MapComponent, MapController } from '@bdmap/map_walkride_search';
import { PoiSearch } from '@bdmap/map_walkride_search';

// ✅ 使用独立包时：
import { MapComponent, MapController } from '@bdmap/map';
import { PoiSearch } from '@bdmap/search';
```

**注意**：切换包方案后，需要同步修改所有相关的 import 语句。

### 4. 检查与判断流程

在为项目添加百度地图依赖前，Agent **必须**按以下步骤检查：

1. **读取 `oh-package.json5`**：检查 `dependencies` 中是否已存在百度地图相关包。
2. **判断已有包类型**：
   - 若已存在 `@bdmap/map_walkride_search` 或 `@bdmap/navi_map`，则当前项目使用的是**组合包方案**。
   - 若已存在 `@bdmap/base`、`@bdmap/map`、`@bdmap/search`、`@bdmap/util` 中的任意一个，则当前项目使用的是**独立包方案**。
   - 若不存在任何百度地图包，则为**全新接入**，需询问用户选择方案。
3. **遵守互斥规则并自动切换**：
   - 已使用组合包 → 新增依赖只能用同一组合包的包名引入，**不得**新增独立包。
   - 已使用独立包，但新需求需要组合包能力（如需要步行/骑行路线规划需要 `@bdmap/map_walkride_search`，或导航需要 `@bdmap/navi_map`） → **自动执行切换流程**（见下方第 4 步），无需询问用户。
   - 已使用独立包，新需求仍可由独立包满足 → 继续安装独立包。
   - 全新接入 → 根据需求选择一种方案，并在后续开发中保持一致。

### 4.1 自动切换流程（独立包 → 组合包）

当项目已安装独立包，但新需求明确需要组合包才能满足时，Agent **必须自动执行**以下切换步骤，无需额外询问用户：

**步骤 1：卸载全部已有的独立包**

从 `oh-package.json5` 的 `dependencies` 中移除所有已安装的百度地图独立包（`@bdmap/base`、`@bdmap/map`、`@bdmap/search`、`@bdmap/util`），然后执行卸载：

```bash
ohpm uninstall @bdmap/base @bdmap/map @bdmap/search @bdmap/util
```

> **注意**：`@bdmap/locsdk` 不需要卸载，它可与组合包共存。

**步骤 2：安装目标组合包**

```bash
ohpm install @bdmap/map_walkride_search
# 或
ohpm install @bdmap/navi_map
```

**步骤 3：批量替换 import 语句**

扫描项目中所有 `.ets` / `.ts` 源文件，将独立包的 import 路径替换为组合包路径。替换映射关系：

| 原 import 来源（独立包） | 替换为（组合包） |
| --- | --- |
| `from '@bdmap/base'` | `from '<组合包名>'` |
| `from '@bdmap/map'` | `from '<组合包名>'` |
| `from '@bdmap/search'` | `from '<组合包名>'` |
| `from '@bdmap/util'` | `from '<组合包名>'` |

其中 `<组合包名>` 为实际安装的组合包，如 `@bdmap/map_walkride_search` 或 `@bdmap/navi_map`。

示例：

```ts
// 切换前（独立包）
import { MapComponent, MapController } from '@bdmap/map';
import { PoiSearch } from '@bdmap/search';
import { DistanceUtil } from '@bdmap/util';

// 切换后（组合包 @bdmap/map_walkride_search）
import { MapComponent, MapController } from '@bdmap/map_walkride_search';
import { PoiSearch } from '@bdmap/map_walkride_search';
import { DistanceUtil } from '@bdmap/map_walkride_search';
```

> `@bdmap/locsdk` 的 import 保持不变，无需替换。

**步骤 4：执行构建验证**

完成切换后，执行 `ohpm install` + 构建命令，确保无编译错误：

```bash
ohpm install && hvigorw assembleHap --mode module -p product=default -p buildMode=debug --no-daemon
```

### 5. 场景选择建议

| 场景 | 推荐方案 | 理由 |
| --- | --- | --- |
| 需要地图 + 检索 + 步行/骑行路线规划 | 组合包 `@bdmap/map_walkride_search` | 增加步行/骑行导航能力 |
| 需要导航 + 地图能力 | 组合包 `@bdmap/navi_map` | 一次安装包含全部能力 |
| 仅需要地图展示，无检索/路线需求 | 独立包 `@bdmap/base` + `@bdmap/map` | 按需引入，减小包体积 |
| 仅需要检索能力，无地图 UI | 独立包 `@bdmap/base` + `@bdmap/search` | 按需引入，减小包体积 |
| 需要定位能力 | 独立包 `@bdmap/locsdk`（可与任何方案搭配） | 定位包独立于组合包体系 |
