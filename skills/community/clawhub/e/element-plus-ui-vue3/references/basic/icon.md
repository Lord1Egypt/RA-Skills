---
name: "icon"
description: "Icon 图标 -- Element Plus Vue3 桌面端组件。Invoke when user needs Icon 图标 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/icon.html"
---

---

# Icon 图标 [​](#icon-图标)

更新日志待解决

15

Element Plus 提供了一套常用的图标集合。

## 使用图标 [​](#使用图标)

-   如果你想像用例一样**直接使用**，你需要[全局注册组件](https://v3.vuejs.org/guide/component-registration.html#global-registration)，才能够直接在项目里使用。

-   如若需要查看所有可用的 SVG 图标请查阅 [@element-plus/icons-vue@1.x](https://unpkg.com/browse/@element-plus/icons-vue@1/dist/es/)[@element-plus/icons-vue@latest](https://unpkg.com/browse/@element-plus/icons-vue@latest/dist/types/components/) 和有关 [Icon Collection](#icon-collection) 的源码 [element-plus-icons](https://github.com/element-plus/element-plus-icons)

## 安装 [​](#安装)

### 使用包管理器 [​](#使用包管理器)

# 选择一个你喜欢的包管理器 [​](#选择一个你喜欢的包管理器)

npmyarnpnpm

shell

```
$ npm install @element-plus/icons-vue
```

shell

```
$ yarn add @element-plus/icons-vue
```

shell

```
$ pnpm install @element-plus/icons-vue
```

### 注册所有图标 [​](#注册所有图标)

您需要从 `@element-plus/icons-vue` 中导入所有图标并进行全局注册。

ts

```
// main.ts

// 如果您正在使用CDN引入，请删除下面一行。
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
```

您也可以参考 [此模板](https://codepen.io/sxzz/pen/xxpvdrg)。

### 浏览器直接引入 [​](#浏览器直接引入)

直接通过浏览器的 HTML 标签导入 Element Plus，然后就可以使用全局变量 `ElementPlusIconsVue`了。

根据不同的 CDN 提供商有不同的引入方式， 根据不同的 CDN 提供商有不同的引入方式， 我们在这里以 [unpkg](https://unpkg.com/) 和 [jsDelivr](https://jsdelivr.com/) 举例。 你也可以使用其它的 CDN 供应商。

unpkgjsDelivr

html

```
<script src="//unpkg.com/@element-plus/icons-vue"></script>
```

html

```
<script src="//cdn.jsdelivr.net/npm/@element-plus/icons-vue"></script>
```

TIP

我们建议使用 CDN 引入 Element Plus 的用户在链接地址上锁定版本，以免将来 Element Plus 升级时受到非兼容性更新的影响。 锁定版本的方法请查看 [unpkg.com](https://unpkg.com/)。

### 自动导入 [​](#自动导入)

使用 [unplugin-icons](https://github.com/antfu/unplugin-icons) 和 [unplugin-auto-import](https://github.com/antfu/unplugin-auto-import) 从 iconify 中自动导入任何图标集。 您可以参考[此模板](https://github.com/sxzz/element-plus-best-practices/blob/db2dfc983ccda5570033a0ac608a1bd9d9a7f658/vite.config.ts#L21-L58)。

## 基础用法 [​](#基础用法)

WARNING

由于 HTML 标准已经定义了一个名为 [menu](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/menu) 的标签，如果你注册的 `Menu` 无法正常工作，则需要使用别名来渲染图标。

vue

```
<!-- 使用 el-icon 为 SVG 图标提供属性 -->
<template>
  <div>
    <el-icon :size="size" :color="color">
      <Edit />
    </el-icon>
    <!-- 或者独立使用它，不从父级获取属性 -->
    <Edit />
  </div>
</template>
```

## 结合 el-icon 使用 [​](#结合-el-icon-使用)

`el-icon` 为原始的 SVG 图标提供额外的属性，细节如下。

vue

```
<template>
  <p>
    with extra class <b>is-loading</b>, your icon is able to rotate 360 deg in 2
    seconds, you can also override this
  </p>
  <el-icon :size="20">
    <Edit />
  </el-icon>
  <el-icon color="#409efc" class="no-inherit">
    <Share />
  </el-icon>
  <el-icon>
    <Delete />
  </el-icon>
  <el-icon class="is-loading">
    <Loading />
  </el-icon>
  <el-button type="primary">
    <el-icon style="vertical-align: middle">
      <Search />
    </el-icon>
    <span style="vertical-align: middle"> Search </span>
  </el-button>
</template>
```

通过添加额外的类名 **is-loading**，你的图标就可以在 2 秒内旋转 360 度，当然你也可以自己改写想要的动画。

搜索

## 直接使用 SVG 图标 [​](#直接使用-svg-图标)

vue

```
<template>
  <div style="font-size: 20px">
    <!-- 由于SVG图标默认不携带任何属性 -->
    <!-- 你需要直接提供它们 -->
    <Edit style="width: 1em; height: 1em; margin-right: 8px" />
    <Share style="width: 1em; height: 1em; margin-right: 8px" />
    <Delete style="width: 1em; height: 1em; margin-right: 8px" />
    <Search style="width: 1em; height: 1em; margin-right: 8px" />
  </div>
</template>
```

## 图标集合 [​](#icon-collection)

TIP

只要你安装了 @element-plus/icons-vue，**就可以在任意版本里使用 SVG 图标**。

**您可以点击图标复制代码**

Copy SVG contentCopy icon code

System

-   Plus
-   Minus
-   CirclePlus
-   Search
-   Female
-   Male
-   Aim
-   House
-   FullScreen
-   Loading
-   Link
-   Service
-   Pointer
-   Star
-   Notification
-   Connection
-   ChatDotRound
-   Setting
-   Clock
-   Position
-   Discount
-   Odometer
-   ChatSquare
-   ChatRound
-   ChatLineRound
-   ChatLineSquare
-   ChatDotSquare
-   View
-   Hide
-   Unlock
-   Lock
-   RefreshRight
-   RefreshLeft
-   Refresh
-   Bell
-   MuteNotification
-   User
-   Check
-   CircleCheck
-   Warning
-   CircleClose
-   Close
-   PieChart
-   More
-   Compass
-   Filter
-   Switch
-   Select
-   SemiSelect
-   CloseBold
-   EditPen
-   Edit
-   Message
-   MessageBox
-   TurnOff
-   Finished
-   Delete
-   Crop
-   SwitchButton
-   Operation
-   Open
-   Remove
-   ZoomOut
-   ZoomIn
-   InfoFilled
-   CircleCheckFilled
-   SuccessFilled
-   WarningFilled
-   CircleCloseFilled
-   QuestionFilled
-   WarnTriangleFilled
-   UserFilled
-   MoreFilled
-   Tools
-   HomeFilled
-   Menu
-   UploadFilled
-   Avatar
-   HelpFilled
-   Share
-   StarFilled
-   Comment
-   Histogram
-   Grid
-   Promotion
-   DeleteFilled
-   RemoveFilled
-   CirclePlusFilled

Arrow

-   ArrowLeft
-   ArrowUp
-   ArrowRight
-   ArrowDown
-   ArrowLeftBold
-   ArrowUpBold
-   ArrowRightBold
-   ArrowDownBold
-   DArrowRight
-   DArrowLeft
-   Download
-   Upload
-   Top
-   Bottom
-   Back
-   Right
-   TopRight
-   TopLeft
-   BottomRight
-   BottomLeft
-   Sort
-   SortUp
-   SortDown
-   Rank
-   CaretLeft
-   CaretTop
-   CaretRight
-   CaretBottom
-   DCaret
-   Expand
-   Fold

Document

-   DocumentAdd
-   Document
-   Notebook
-   Tickets
-   Memo
-   Collection
-   Postcard
-   ScaleToOriginal
-   SetUp
-   DocumentDelete
-   DocumentChecked
-   DataBoard
-   DataAnalysis
-   CopyDocument
-   FolderChecked
-   Files
-   Folder
-   FolderDelete
-   FolderRemove
-   FolderOpened
-   DocumentCopy
-   DocumentRemove
-   FolderAdd
-   FirstAidKit
-   Reading
-   DataLine
-   Management
-   Checked
-   Ticket
-   Failed
-   TrendCharts
-   List

Media

-   Microphone
-   Mute
-   Mic
-   VideoPause
-   VideoCamera
-   VideoPlay
-   Headset
-   Monitor
-   Film
-   Camera
-   Picture
-   PictureRounded
-   Iphone
-   Cellphone
-   VideoCameraFilled
-   PictureFilled
-   Platform
-   CameraFilled
-   BellFilled

Traffic

-   Location
-   LocationInformation
-   DeleteLocation
-   Coordinate
-   Bicycle
-   OfficeBuilding
-   School
-   Guide
-   AddLocation
-   MapLocation
-   Place
-   LocationFilled
-   Van

Food

-   Watermelon
-   Pear
-   NoSmoking
-   Smoking
-   Mug
-   GobletSquareFull
-   GobletFull
-   KnifeFork
-   Sugar
-   Bowl
-   MilkTea
-   Lollipop
-   Coffee
-   Chicken
-   Dish
-   IceTea
-   ColdDrink
-   CoffeeCup
-   DishDot
-   IceDrink
-   IceCream
-   Dessert
-   IceCreamSquare
-   ForkSpoon
-   IceCreamRound
-   Food
-   HotWater
-   Grape
-   Fries
-   Apple
-   Burger
-   Goblet
-   GobletSquare
-   Orange
-   Cherry

Items

-   Printer
-   Calendar
-   CreditCard
-   Box
-   Money
-   Refrigerator
-   Cpu
-   Football
-   Brush
-   Suitcase
-   SuitcaseLine
-   Umbrella
-   AlarmClock
-   Medal
-   GoldMedal
-   Present
-   Mouse
-   Watch
-   QuartzWatch
-   Magnet
-   Help
-   Soccer
-   ToiletPaper
-   ReadingLamp
-   Paperclip
-   MagicStick
-   Basketball
-   Baseball
-   Coin
-   Goods
-   Sell
-   SoldOut
-   Key
-   ShoppingCart
-   ShoppingCartFull
-   ShoppingTrolley
-   Phone
-   Scissor
-   Handbag
-   ShoppingBag
-   Trophy
-   TrophyBase
-   Stopwatch
-   Timer
-   CollectionTag
-   TakeawayBox
-   PriceTag
-   Wallet
-   Opportunity
-   PhoneFilled
-   WalletFilled
-   GoodsFilled
-   Flag
-   BrushFilled
-   Briefcase
-   Stamp

Weather

-   Sunrise
-   Sunny
-   Ship
-   MostlyCloudy
-   PartlyCloudy
-   Sunset
-   Drizzling
-   Pouring
-   Cloudy
-   Moon
-   MoonNight
-   Lightning

Other

-   ChromeFilled
-   Eleme
-   ElemeFilled
-   ElementPlus
-   Shop
-   SwitchFilled
-   WindPower

## API [​](#api)

### Attributes [​](#attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| color | svg 的 fill 颜色 | `string` | 继承颜色 |
| size | SVG 图标的大小，size x size | `number` / `string` | 继承字体大小 |

### Slots [​](#slots)

| 名称 | 说明 |
| --- | --- |
| default | 自定义默认内容 |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/icon) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/icon.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/icon.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/128720752?v=4&size=64)](https://github.com/cjn021)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/27912232?v=4&size=64)](https://github.com/Fuphoenixes)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/21235555?v=4&size=64)](https://github.com/zhangenming)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/4318293?v=4&size=64)](https://github.com/cn-troy)[![](https://avatars.githubusercontent.com/u/134276765?v=4&size=64)](https://github.com/zwgwf)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/10731096?v=4&size=64)](https://github.com/zazzaz)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/56141625?v=4&size=64)](https://github.com/micaiguai)[![](https://avatars.githubusercontent.com/u/20151622?v=4&size=64)](https://github.com/william-xue)[![](https://avatars.githubusercontent.com/u/117748716?v=4&size=64)](https://github.com/thinkasany)[![](https://avatars.githubusercontent.com/u/25273880?v=4&size=64)](https://github.com/basonwoo)[![](https://avatars.githubusercontent.com/u/24582461?v=4&size=64)](https://github.com/KevinLjb)[![](https://avatars.githubusercontent.com/u/17680888?v=4&size=64)](https://github.com/iamkun)[![](https://avatars.githubusercontent.com/u/19891724?v=4&size=64)](https://github.com/pdsuwwz)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)

[Container 布局容器](https://element-plus.org/zh-CN/component/container)

[Layout 布局](https://element-plus.org/zh-CN/component/layout)


