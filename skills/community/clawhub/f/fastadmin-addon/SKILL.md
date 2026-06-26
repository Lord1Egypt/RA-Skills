---
name: fastadmin-addon
description: FastAdmin插件开发助手。用于创建、开发和打包FastAdmin应用插件。当用户需要创建FastAdmin插件、开发插件功能、配置插件菜单、数据库、打包插件时使用此skill。支持生成插件目录结构、控制器、模型、视图、配置文件、菜单配置、数据库脚本等。
---

# FastAdmin插件开发

本skill帮助开发者快速创建和开发FastAdmin应用插件。

## 快速开始

### 创建新插件

使用命令行创建插件基础结构：

```bash
cd /var/www/yoursite
php think addon -a <插件标识> -c create
```

插件标识规则：
- 只能使用小写字母，至少3个字符
- 建议使用英文单词或拼音首字母
- 先在 https://www.fastadmin.net/developer/idcheck.html 检测标识是否可用

### 插件目录结构

创建后的插件位于 `addons/<插件标识>/`，基础结构如下：

```
mydemo/
├── Mydemo.php          # 插件核心安装卸载控制器（必需，首字母大写）
├── config.php          # 插件配置文件
├── info.ini            # 插件信息文件（必需）
├── install.sql         # 数据库安装脚本（可选）
├── testdata.sql        # 测试数据脚本（可选）
├── bootstrap.js        # JS启动文件（可选）
├── config.html         # 自定义配置视图（可选）
├── LICENSE             # 版权文件
├── controller/         # 前台控制器目录
├── model/              # 模型目录
├── view/               # 视图目录
├── lang/               # 语言包目录
├── library/            # 类库目录
├── assets/             # 静态资源（会复制到/public/assets/addons/插件标识/）
├── application/        # 后台应用文件（会覆盖到/application）
│   └── admin/
│       ├── controller/<插件标识>/
│       ├── model/<插件标识>/
│       └── view/<插件标识>/
└── public/             # 公共资源（会覆盖到/public）
    └── assets/js/backend/<插件标识>/
```

## 核心文件说明

### info.ini - 插件信息

```ini
name = mydemo
title = 示例插件
intro = 这是一个示例插件的介绍
author = FastAdmin
website = https://www.fastadmin.net
version = 1.0.0
state = 1
```

### Mydemo.php - 插件核心类

```php
<?php
namespace addons\mydemo;

use app\common\library\Menu;
use think\Addons;

class Mydemo extends Addons
{
    protected $menu = [
        [
            'name' => 'mydemo',
            'title' => 'Mydemo管理',
            'icon' => 'fa fa-map-marker',
            'ismenu' => 1,
            'weigh' => 1,
            'sublist' => [
                ["name" => "mydemo/index/index", "title" => "查看"],
                ["name" => "mydemo/index/add", "title" => "添加"],
                ["name" => "mydemo/index/edit", "title" => "编辑"],
                ["name" => "mydemo/index/del", "title" => "删除"],
            ]
        ]
    ];

    public function install()
    {
        Menu::create($this->menu);
        return true;
    }

    public function uninstall()
    {
        Menu::delete("mydemo");
        return true;
    }

    public function enable()
    {
        Menu::enable("mydemo");
        return true;
    }

    public function disable()
    {
        Menu::disable("mydemo");
        return true;
    }

    public function upgrade()
    {
        Menu::upgrade('mydemo', $this->menu);
        return true;
    }
}
```

### config.php - 插件配置

```php
<?php
return [
    [
        'name' => 'yourname',
        'title' => '配置标题',
        'type' => 'string',
        'group' => '',
        'content' => [],
        'value' => '',
        'rule' => 'required',
        'msg' => '',
        'tip' => '',
        'ok' => '',
        'extend' => ''
    ],
];
```

配置类型支持：string/text/number/datetime/array/select/selects/image/images/file/files/checkbox/radio/bool

### 前台控制器

```php
<?php
namespace addons\mydemo\controller;

use think\addons\Controller;

class Index extends Controller
{
    protected $noNeedLogin = ['*'];  // 无需登录的方法
    protected $noNeedRight = ['*'];  // 无需鉴权的方法

    public function index()
    {
        return $this->fetch();
    }
}
```

访问地址：`http://www.example.com/addons/mydemo/index/index`

### 后台控制器

位于 `application/admin/controller/<插件标识>/` 目录：

```php
<?php
namespace app\admin\controller\mydemo;

use app\common\controller\Backend;

class Test extends Backend
{
    public function index()
    {
        // CRUD列表逻辑
    }
}
```

### 数据库脚本 install.sql

```sql
CREATE TABLE IF NOT EXISTS `__PREFIX__mydemo_list` (
  `id` int(10) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `title` varchar(100) DEFAULT NULL COMMENT '标题',
  `createtime` bigint(16) DEFAULT NULL COMMENT '创建时间',
  `updatetime` bigint(16) DEFAULT NULL COMMENT '更新时间',
  `status` enum('normal','hidden') NOT NULL DEFAULT 'normal' COMMENT '状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='示例表';
```

使用 `__PREFIX__` 表示数据库表前缀，安装时自动替换。

## 数据库设计规范

- 表名和字段名全小写，只允许a-z和_，不能有拼音
- 存储引擎统一使用InnoDB
- 字符集统一使用utf8mb4，排序规则utf8mb4_general_ci
- 关联字段统一使用_id结尾
- 时间统一使用Unix时间戳格式，bigint(16)，以time结尾
- 主键必须为id
- 表名必须以插件标识开头，如：`__PREFIX__mydemo_log`

特殊字段建议：
- `category_id` - 分类ID，后台CRUD自动生成selectpage组件
- `user_id` - 会员ID，后台CRUD自动生成selectpage组件
- `weigh` - 权重，后台排序字段
- `createtime/updatetime/deletetime` - 创建/更新/删除时间
- `status` - 状态字段，启用TAB选项卡展示

## 打包插件

### 命令行打包（推荐）

```bash
cd /var/www/yoursite
php think addon -a mydemo -c package
```

打包后的文件位于：`runtime/addons/mydemo-1.0.0.zip`

### 打包注意事项

- 不要在addons目录下直接压缩插件目录
- 移除无关文件：.addonrc、.DS_Store、.git、.svn等
- 移除插件包中的调试代码、注释、测试资源
- application不允许新增其他模块，只允许index/api/admin
- public和assets目录下不允许任何php/asp/jsp等服务端脚本

## 常用函数

```php
// 读取插件配置
$config = get_addon_config('插件标识');

// 读取完整配置
$fullconfig = get_addon_fullconfig('插件标识');

// 更新插件配置
set_addon_config('插件标识', $config, true);
set_addon_fullconfig('插件标识', $config);

// 检查插件是否存在
if (is_dir(ADDON_PATH . 'mydemo')) {
    // 插件存在
}
```

## 视图中的路径

- `__ADDON__` - 指向 `/public/assets/addons/插件标识/`

## 参考文档

详细开发文档请参考：
- [FastAdmin插件开发文档](https://doc.fastadmin.net/developer/55.html)
