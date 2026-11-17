---
name: "empirecms7.5-php8-upgrade"
description: "帝国CMS 7.5 升级到 PHP 8 兼容性修改清单。当用户需要将帝国CMS 7.5 升级到 PHP 8、修复 PHP 8 致命错误、或从 PHP 7.x 迁移到 PHP 8 时调用。"
version: "1.0.2"
author: "智慧半岛"
---

# 帝国CMS 7.5 PHP 8 兼容性升级技能

本技能提供帝国CMS 7.5 升级到完全兼容 PHP 8.x 的系统方法论。基于对 PHP8 兼容原版与 PHP7.4 二次开发版的差异对比总结。

## 何时调用

- 用户需要将帝国CMS 7.5 升级到 PHP 8
- 用户报告 PHP 8 致命错误（白屏、TypeError、Fatal Error 等）
- 用户需要修复帝国CMS的 PHP 8 兼容性问题
- 用户询问 php8_count、get_magic_quotes_gpc、preg_replace /e、create_function、split、字符串比较异常等问题

## 执行流程

### Step 1: 确认项目路径与状态

解析用户输入，定位帝国CMS项目根目录。若用户未提供路径，主动索取。确认以下信息后进入下一步：
- 项目根路径（用于定位 `e/class/connect.php` 等文件）
- PHP 版本（确认是否为 PHP 8.x）
- 是否已有 `bat_7.5/` 备份目录

### Step 2: 按优先级分级执行修复

严格按照 P0（致命错误） → P1（严重警告） → P2（兼容性优化）顺序执行，每完成一个文件修复即提示用户验证，验证通过后再继续下一文件。P0 阶段的目标是让项目能在 PHP 8 下启动（不再白屏）。

### Step 3: 按模板执行每项修改

下文「核心修改方法」章节中每个编号小节即为一项修改模板。执行时：
- 读取目标文件的对应行号范围
- 与模板中的「修改前」代码对比确认
- 执行替换为「修改后」代码
- 告知用户修改了哪个文件的哪几行

### Step 4: 输出修改汇总

所有修复完成后，输出已完成修改的文件清单、修改量统计和验证测试建议。

## Init-Step-Poll 渐进式防卡死协议

帝国CMS PHP 8 升级属于长任务，涉及大批量 PHP 文件扫描、逐文件修复、日志复核和人工验证。遇到目录级扫描、批量修复、全站兼容检查或生成静态页相关任务时，必须采用 Init → Step → Poll 渐进式执行，避免一次性长时间运行导致卡死或无法定位失败点。

| 阶段 | 动作 | 输出 | 失败回退 |
|:---|:---|:---|:---|
| Init | 确认项目根目录、PHP 版本、备份状态、排除目录和修复范围 | `task_id`、文件清单、P0/P1/P2 队列、当前进度 `0/N` | 路径、备份或 PHP 版本不满足时停止，要求用户补充 |
| Step | 每次只处理 1 个文件或 1 个小模块，完成读取、定位、修改、lint/日志检查 | 当前文件、修改点、验证命令、下一待处理文件 | 单文件失败时记录失败原因，跳过后续批量修改，转人工确认 |
| Poll | 查询任务状态，汇总已完成/失败/待处理数量和最近一次验证结果 | `running/success/failed/paused`、进度百分比、失败清单 | 状态异常时回到最近一个已验证文件，不继续扩大修改范围 |

执行约束：

- Init 阶段必须排除 `data/dbcache/`、`data/fc/`、`runtime/`、`e/tmp/`、`uploads/`、`d/file/`、`backup/`、`vendor/`、`.git/`。
- Step 阶段禁止跨文件批量替换；数组键、`count()`、`each()`、`preg_replace /e`、`create_function()` 等同类问题必须在当前文件内一次性修完。
- 每个 Step 完成后必须给出验证证据：PHP lint、错误日志片段、页面/API 手动验证步骤或用户确认。
- Poll 阶段不得把未验证文件计入完成数；进度只能按“已验证文件数 / 总文件数”计算。
- 长任务中断后必须从 Poll 的失败清单和最后一个已验证文件恢复，不得从头重复覆盖。

## 约束规则

1. **备份优先**：修改任何文件前，必须先确认项目已有备份
2. **逐文件验证**：每完成一个文件的全部修改后提示用户测试，避免批量修改导致难以定位问题
3. **禁止批量替换数组键**：必须逐行检查 `$var[key]`，对 `$var[$i]`、`$var[0]`、`$var[常量]` 模式跳过不替换，仅对字符串字面量键名加单引号
4. **禁止直接文件覆盖**：以用户项目文件为基础修改，不得用参考版文件直接覆盖
5. **注意文件编码**：帝国CMS 文件使用 GBK 编码，读取/写入均需保持编码不变
6. **输入不足时主动索取**：项目路径缺失时向用户索取，不得猜测路径

## 能力边界

| 能力 | 说明 |
|------|------|
| 能做 | 按优先级逐文件执行 PHP 8 兼容性修复（connect.php、数组键加引号、count() 替换、each()→foreach、preg_replace /e、create_function、split 等） |
| 能做 | 对照已有差异模板精确定位修改行号并执行替换 |
| 能做 | 输出修改汇总和验证测试建议 |
| 有限度能做 | 二次开发模块（e/article/、e/dongpo/、e/admin/sinfo/）需逐文件审查后修复，无法预估全部定制逻辑 |
| 不能做 | 批量自动化替换（数组键必须逐行人工判断变量/常量/字面量） |
| 不能做 | 在无项目路径的情况下凭空修改 |
| 不能做 | 处理帝国CMS 7.5 以外的版本或非 PHP 8 兼容性问题 |

---

##  当前项目状态速览（127.0.2.100）

| 检查项                       | 状态                               | 影响                                            |
| ---------------------------- | ---------------------------------- | ----------------------------------------------- |
| connect.php error_reporting  |  缺少 ^E_DEPRECATED              | PHP 8 弃用警告破坏输出                          |
| connect.php MAGIC_QUOTES_GPC |  使用 ini_set 错误写法           | PHP 8 致命错误（magic_quotes_runtime 已移除）   |
| connect.php php8_count()     |  完全缺失                        | count() 对 null/非数组参数抛出 TypeError        |
| 数组键加引号                 |  11,000+ 处未加引号              | PHP 8 中 `$var[key]` 视为常量，抛出 Fatal Error |
| e/article/ 目录              |  二次开发独有目录                | 对应原版 e/action/，需单独检查修复              |
| e/article/list.php           |  数组键已加引号（代码质量好）    | 需检查 count() 和 SQL 语法                      |
| e/article/show.php           |  有未加引号数组键 + count() 问题 | 需修复第 94、136、204、225、296、374、386 行    |

### 当前 connect.php 问题定位

```php
//  第2行：缺少 ^E_DEPRECATED
error_reporting(E_ALL ^ E_NOTICE);

//  第6行：已有正确写法（被注释掉了！）
//define('MAGIC_QUOTES_GPC',function_exists('get_magic_quotes_gpc')&&get_magic_quotes_gpc());

//  第7行：错误写法（PHP 8 致命错误）
define('MAGIC_QUOTES_GPC',ini_set("magic_quotes_runtime",0)?True:False);
// 问题：ini_set() 返回的是原来的值（字符串），不是布尔值
// 问题：magic_quotes_runtime 在 PHP 8 中已完全移除，调用会报错

//  缺少：php8_count() 函数定义
```

### e/article/show.php 问题定位

```php
//  第94行：SQL 字符串中数组键未加引号
$finfor = $empire->fetch1("select ... from {$dbtbpre}ecms_" . $tbname . "_data_" . $r['stb'] . " where id='$r[id]' limit 1");
//                                                              ^^^^^ 应改为 {$r['id']}

//  第136行：SQL 字符串中数组键未加引号
$newstemp_r = $empire->fetch1("select ... where tempid='$r[newstempid]'");
//                                                         ^^^^^ 应改为 {$r['newstempid']}

//  第204行：SQL 字符串中数组键未加引号
$empire->query("update ... set onclick=onclick+1 where id='$add[id]' limit 1");
//                                                                ^^^^^ 应改为 {$add['id']}

//  第225行：count() 可能需要替换
$thispagenum = count($n_r);
// 考虑改为：$thispagenum = php8_count($n_r);

//  第296行：count() 可能需要替换
$fcount = count($fr) - 1;
// 考虑改为：$fcount = php8_count($fr) - 1;

//  第374、386行：SQL 中 $add[id] 和 $add[classid] 未加引号
```

---

##  100版 vs 101版 核心文件差异对比（）

基于对 `127.0.2.100`（PHP7.4 二次开发版）与 `127.0.2.101`（PHP8 兼容原版）的目录级扫描与核心文件内容对比，以下是关键差异统计：

### 核心文件 PHP 8 兼容性问题对比表

| 文件                          | 问题类型          | 100版（PHP7.4）           | 101版（PHP8）                 | 需修复        |
| ----------------------------- | ----------------- | ------------------------- | ----------------------------- | ------------- |
| **e/class/connect.php**       | php8_count() 定义 |  完全缺失               |  第5431行定义函数           | 必须添加      |
| **e/class/connect.php**       | php8_count() 使用 | 0 处                      |  30+ 处使用                 | 需替换        |
| **e/class/connect.php**       | error_reporting   |  缺 `^E_DEPRECATED`     |  已包含                     | 1 处修改      |
| **e/class/connect.php**       | MAGIC_QUOTES_GPC  |  `ini_set` 错误写法     |  `function_exists` 正确写法 | 1 处修改      |
| **e/class/functions.php**     | php8_count() 使用 | 0 处                      |  46 处使用                  | 需替换 ~46 处 |
| **e/class/functions.php**     | count() 总调用    | 70 处                     | 70 处（部分已替换）           | 判断性替换    |
| **e/class/doiconv.php**       | each() 使用       |  6 处活跃使用           |  0 处（已替换为 foreach）   | 6 处必须替换  |
| **e/class/SendEmail.inc.php** | preg_replace /e   |  2 处（第1244、1247行） |  2 处（原版未修复）         | 2 处必须替换  |
| **e/class/classfun.php**      | count() 调用      | 16 处                     | 16 处                         | 判断性替换    |
| **e/class/hinfofun.php**      | count() 调用      | 24 处                     | 24 处                         | 判断性替换    |
| **e/class/moddofun.php**      | count() 调用      | 34 处                     | 34 处                         | 判断性替换    |

### connect.php 差异详解

**101版 php8_count() 函数定义**（文件末尾第5431行）：

```php
// 为了count for php8
function php8_count($a){
    return is_array($a)?count($a):0;
}
```

**100版需做的3处修改**：

1. 第2行：添加 `^E_DEPRECATED` 到 error_reporting
2. 第7行：将 `ini_set("magic_quotes_runtime",0)` 改为 `function_exists('get_magic_quotes_gpc') && get_magic_quotes_gpc()`
3. 文件末尾 `?>` 之前：添加 `php8_count()` 函数定义

---

### doiconv.php 的 each() 替换参考

**100版 doiconv.php 中的 each() 使用位置**：
| 行号 | 代码模式 | 问题 |
|------|---------|------|
| ~142 | `while(list($key,$value)=each($tmp))` | PHP 8 致命错误 |
| ~165 | `while(list($key,$value)=each($tmp))` | PHP 8 致命错误 |
| ~177 | `while(list($key,$value)=each($tmp))` | PHP 8 致命错误 |
| ~208 | `while(list($key,$value)=each($tmp))` | PHP 8 致命错误 |
| ~222 | `while(list($key,$value)=each($tmp))` | PHP 8 致命错误 |

**101版的修复模式**（第129-130行可见范例）：

```php
//  100版
while(list($key,$value)=each($tmp))
// ... 处理逻辑

//  101版 - 注释掉each，改用foreach
// while(list($key,$value)=each($tmp))
foreach($tmp as $key=>$value)
// ... 处理逻辑保持不变
```

---

### SendEmail.inc.php preg_replace /e 问题

两个版本都存在此问题（原版也未完全修复）。需手动替换：

**第1244行**：

```php
//  修改前
$encoded = preg_replace("/([\001-\010\013\014\016-\037\075\177-\377])/e",
    'sprintf("=%02X", ord("\\1"))', $encoded);

//  修改后
$encoded = preg_replace_callback(
    "/([\001-\010\013\014\016-\037\075\177-\377])/",
    function($m) { return '=' . sprintf('%02X', ord($m[1])); },
    $encoded
);
```

**第1247行**：同理替换

---

### 100版独有目录与文件检查清单

以下目录/文件是 100版独有或二次开发重命名的，需独立检查，不能直接参考 101版：

| 目录/文件                | 状态                              | 检查重点                                                             |
| ------------------------ | --------------------------------- | -------------------------------------------------------------------- |
| `e/article/`             |  独有目录（对应原版 e/action/） | 所有 PHP 文件的数组键、count()、SQL 语法                             |
| `e/article/list.php`     |  独有文件                       | 自定义分页逻辑、count() 调用                                         |
| `e/article/show.php`     |  独有文件                       | 未加引号数组键（94/136/204/374/386行）、count()（225/234/255/296行） |
| `e/admin/sinfo/`         |  独有二次开发目录               | dp_funs.php（6处count）、listinfo.php、set.php（12处count）          |
| `e/dongpo/`              |  二次开发模块                   | 所有 PHP 文件的数组键                                                |
| `e/admin/clean_7890.php` |  独有文件                       | 清理脚本，检查 PHP 8 语法                                            |

**e/admin/sinfo/ 目录具体检查提示**：

- `dp_funs.php`: 6 处 count() 调用 → 检查是否需要 php8_count()
- `listinfo.php`: 1 处 count() + 数组键检查
- `set.php`: 12 处 count() + 数组键检查
- `cidtype.php`: 2 处 count() 调用
- `push.php`: 1 处 count() 调用

---

### 目录结构差异速查

| 路径            | 100版（PHP7.4）  | 101版（PHP8） | 说明                                   |
| --------------- | ---------------- | ------------- | -------------------------------------- |
| 前台动态页目录  | `e/article/`     | `e/action/`   | 100版重命名，含独有 list.php、show.php |
| 后台 sinfo 模块 | `e/admin/sinfo/` |  不存在     | 100版二次开发模块                      |
| 核心类库        | `e/class/`       | `e/class/`    | 基本一致，含 pinyin.php（100独有）     |
| 备份目录        | `bat_7.5/`       |  不存在     | 100版自己的备份，可作为恢复参考        |

---

##  核心修改方法（按优先级排序）

### P0：致命错误 - 必须首先修复（导致白屏/500）

#### 1. 修复 connect.php - 核心兼容性（3处修改）

**位置：`e/class/connect.php`**

修改1：error_reporting 增加 ^E_DEPRECATED

```php
//  修改前（第2行）
error_reporting(E_ALL ^ E_NOTICE);

//  修改后
error_reporting(E_ALL ^ E_NOTICE ^ E_DEPRECATED);
```

修改2：修复 MAGIC_QUOTES_GPC 定义

```php
//  修改前（第7行）
define('MAGIC_QUOTES_GPC',ini_set("magic_quotes_runtime",0)?True:False);

//  修改后（直接启用第6行的正确写法，或替换第7行为）
define('MAGIC_QUOTES_GPC', function_exists('get_magic_quotes_gpc') && get_magic_quotes_gpc());
```

修改3：在文件末尾（`?>` 之前）添加 php8_count() 函数

```php
//  在文件末尾添加（PHP 8 count() 兼容包装函数）
function php8_count($a) {
    return is_array($a) ? count($a) : 0;
}
```

**重要提示**：完成此步骤后，项目应能在 PHP 8 下启动（不再白屏），但仍有大量数组键未加引号的问题需逐文件修复。

---

#### 2. 数组键加引号（最关键、工作量最大）

**问题**：未加引号的数组键如 `$var[key]` 在 PHP 8 中会被当作**常量**解析，常量未定义时抛出 `Error: Undefined constant "key"` 致命错误。

**PHP 7.x vs PHP 8 行为差异**：

| 代码          | PHP 7.x 行为                                             | PHP 8 行为                                           |
| ------------- | -------------------------------------------------------- | ---------------------------------------------------- |
| `$r[wburl]`   | 视为未定义常量，回退为字符串 `'wburl'`（仅 Notice 警告） | 抛出 `Error: Undefined constant "wburl"`（致命错误） |
| `$r['wburl']` |  正常                                                  |  正常                                              |

**加引号的判断原则（必须严格遵守）**

```
遇到 $var[...] 时按以下顺序判断：

1. 括号内是变量（$key、$classid、$i）？ →  不加引号
   正确示例：$r[$key]、$class_r[$classid]、$r[$i]

2. 括号内是数字（0、1、-1）？ →  不加引号
   正确示例：$arr[0]、$list_r[1]

3. 括号内是表达式（$i+1、$page-1）？ →  不加引号
   正确示例：$r[$i+1]

4. 括号内是已定义常量（MY_CONST）？ →  不加引号
   正确示例：$r[ECMS_PATH]（但这种情况极少）

5. 括号内是字符串字面量（wburl、classid、id、title、newsurl）？ →  必须加单引号
   修复：$r[wburl] → $r['wburl']
   修复：$_GET[classid] → $_GET['classid']
   修复：$class_r[$classid][tbname] → $class_r[$classid]['tbname']
```

** 绝对禁止批量替换**：必须逐个文件、逐行检查，避免误改变量键名（如 `$r[$i]` 变成 `$r['$i']` 会造成严重错误）。

**重点文件清单（按修改量排序）**

| 文件/目录                 | 预估修改量 | 典型问题                                                            |
| ------------------------- | ---------- | ------------------------------------------------------------------- |
| `e/class/classfun.php`    | ~1462 处   | `$add[f]`、`$add[keyboard]`、`$add[classid]`                        |
| `e/class/functions.php`   | ~1006 处   | `$r[wburl]`、`$r[newstime]`、`$r[id]`、`$class_r[$classid][tbname]` |
| `e/admin/*.php` 及子目录  | 2000+ 处   | `$add[newsurl]`、`$add[bakdbpath]`、`$add[searchtype]`              |
| `e/dongpo/*.php`          | ~434 处    | 二次开发模块，需特别检查                                            |
| `e/admin/sinfo/*.php`     | ~277 处    | 二次开发模块，需特别检查                                            |
| `e/member/*.php`          | ~337 处    | `$user[userid]`、`$user[username]`                                  |
| `e/article/*.php`         | ~50 处     | 独有文件，详见后文单独分析                                          |
| `e/template/*.php`        | 若干       | 模板相关文件                                                        |
| `e/class/moddofun.php`    | ~865 处    | 大量数组键未加引号                                                  |
| `e/class/hinfofun.php`    | ~630 处    | `$r[userid]`、`$r[filename]`                                        |
| `e/class/cjfun.php`       | ~330 处    | CJ 相关函数                                                         |
| `e/class/t_functions.php` | ~308 处    | 模板函数                                                            |

**修复示例对比**

```php
//  修改前 - 一维数组
$r[wburl]
$r[newstime]
$r[classid]
$r[id]
$_GET[classid]
$_POST[from]

//  修改后
$r['wburl']
$r['newstime']
$r['classid']
$r['id']
$_GET['classid']
$_POST['from']

//  修改前 - 多维数组（最常见的错误模式）
$class_r[$classid][featherclass]
$class_r[$classid][modid]
$class_r[$classid][tbname]
$class_r[$classid][filename]
$class_r[$classid][islast]
$public_r[newsurl]
$emod_r[$mid][tempf]
$ecms_tofunr[cacheuse]

//  修改后 - 多维数组（变量键名不加引号，字符串键名加引号）
$class_r[$classid]['featherclass']
$class_r[$classid]['modid']
$class_r[$classid]['tbname']
$class_r[$classid]['filename']
$class_r[$classid]['islast']
$public_r['newsurl']
$emod_r[$mid]['tempf']
$ecms_tofunr['cacheuse']
```

**完成此步骤的验证方法**：逐文件打开测试，或使用 PHP 8 的 `php -l 文件路径` 进行语法检查（注意：`php -l` 只能检查语法错误，无法检查运行时的常量问题，必须实际运行测试）。

---

#### 3. count() 替换为 php8_count()

**问题**：PHP 8 中 `count()` 对 `null` 或非数组参数抛出 `TypeError: count(): Argument #1 ($value) must be of type Countable|array, null given`。

**解决方案**：使用 connect.php 中新增的 `php8_count()` 函数。

**替换原则（请谨慎判断，不是所有 count() 都需要替换）**

| 场景                                            | 是否替换                            | 示例                                                                   |
| ----------------------------------------------- | ----------------------------------- | ---------------------------------------------------------------------- |
| 变量来源不确定（可能为 null）                   |  替换为 php8_count()              | `count($r)` → `php8_count($r)`                                         |
| 循环中对数组变量计数                            |  替换为 php8_count()              | `for($i=0;$i<count($arr);$i++)` → `for($i=0;$i<php8_count($arr);$i++)` |
| 数组字面量（`count(array(1,2,3))`）             |  保持原样                         | 不需要替换                                                             |
| 明确是数据库查询结果（fetch1/fetch 后立即使用） |  建议替换（数据库查询可能返回空） | `count($r)` → `php8_count($r)`                                         |
| explode() 后立即使用                            |  建议替换                         | `count(explode(',', $str))` → `php8_count(explode(',', $str))`         |

**重点文件清单**

| 文件                               | 预估修改量 | 典型示例                                                            |
| ---------------------------------- | ---------- | ------------------------------------------------------------------- |
| `e/class/functions.php`            | ~46 处     | `count($r)-1`、`count($fr)-1`、`count($dtbr)`                       |
| `e/class/hinfofun.php`             | ~17 处     | `count($n_r)`、`count($copyclassid)`、`count($infoid)`              |
| `e/class/classfun.php`             | ~9 处      | `count($vr)`、`count($myorder)`、`count($groupid)`                  |
| `e/class/moddofun.php`             | ~24 处     | `count($dtbr)`、`count($re)-1`、`for($i=0;$i<count($myorder);$i++)` |
| `e/member/class/member_modfun.php` | ~10 处     | `count($r)`、`count($fr)`、`count($mustr)`                          |
| `e/admin/workflow/ListWfItem.php`  | 2 处       | `count($groupid)`、`count($tid)`                                    |
| `e/member/list/index.php`          | 2 处       | `count($show)`、`count($gr)`                                        |
| `e/article/show.php`               | ~5 处      | `count($n_r)`、`count($ti_r)`、`count($fr)-1`                       |

**修复示例对比**

```php
//  修改前 - 直接 count()
$count = count($r) - 1;
for ($i = 0; $i < count($myorder); $i++) { ... }
$cpcount = count($copyclassid);
$thispagenum = count($n_r);

//  修改后 - 使用 php8_count()
$count = php8_count($r) - 1;
for ($i = 0; $i < php8_count($myorder); $i++) { ... }
$cpcount = php8_count($copyclassid);
$thispagenum = php8_count($n_r);

// ? 特殊情况 - 明确是数组的可以保持 count()
// 如果变量紧跟在 foreach 或 explode 之后，且可以确保是数组，可以保持 count()
// 但为了安全起见，建议全部替换为 php8_count()
```

---

#### 4. SQL 语句花括号语法修复

**问题**：在 SQL 语句（双引号字符串）中直接嵌入数组键时，`'$var[key]'` 在 PHP 8 中会触发未定义常量错误。

**解决方案**：使用花括号语法 `{$var['key']}`，确保数组键在双引号字符串中正确解析。

**修复原则**

```php
//  原写法（PHP 8 致命错误）- 在 SQL 双引号字符串中
$empire->query("select ... where classid='$r[classid]' and id='$r[id]'");
$empire->query("update ... set keyboard='".eaddslashes($add[keyboard])."'");
$empire->query("insert ... values('$r[tagid]','$r[newstime]')");

//  PHP 8 兼容写法 - 数字类型字段用花括号不加引号
$empire->query("select ... where classid={$r['classid']} and id={$r['id']}");
$empire->query("update ... set classid={$add['classid']}");

//  PHP 8 兼容写法 - 字符串类型字段用花括号加引号
$empire->query("update ... set keyboard='".eaddslashes($add['keyboard'])."'");
$empire->query("insert ... values('{$r['tagid']}','{$r['newstime']}')");

//  表名引用也需要修复
//  $class_r[$classid][tbname]
//  $class_r[$classid]['tbname']
```

**典型修复示例（来自 functions.php 和 classfun.php）**

```php
//  修改前
$zinfor = $empire->fetch1("select zid,ztid,cid from {$dbtbpre}enewsztinfo where ztid='$ztid' and classid='$r[classid]' and id='$r[id]' limit 1");

//  修改后
$zinfor = $empire->fetch1("select zid,ztid,cid from {$dbtbpre}enewsztinfo where ztid='$ztid' and classid={$r['classid']} and id={$r['id']} limit 1");

//  修改前
$empire->query("insert into {$dbtbpre}enewsztinfo(ztid,cid,classid,id,newstime,mid,isgood) values('$ztid','$zcid','$r[classid]','$r[id]','$r[newstime]','$mid','0');");

//  修改后
$empire->query("insert into {$dbtbpre}enewsztinfo(ztid,cid,classid,id,newstime,mid,isgood) values('$ztid','$zcid',{$r['classid']},{$r['id']},{$r['newstime']},'$mid','0');");
```

**注意事项**：SQL 语句中的 `{$dbtbpre}` 本身是正确的（它是一个简单变量，不是数组键），不需要修改。需要修改的是 `$r[key]`、`$add[key]` 这一类数组键引用。

---

#### 5. each() 函数替换为 foreach

**问题**：`each()` 函数在 PHP 7.2 中已弃用，在 PHP 8 中已完全移除，调用直接 Fatal Error。

**重点文件**：`e/class/doiconv.php`（约 6 处活跃使用）

**修复模式**

```php
//  修改前
while (list($key, $value) = each($tmp)) {
    // ... 处理逻辑
}

//  修改后
foreach ($tmp as $key => $value) {
    // ... 处理逻辑保持不变
}
```

**检查提示**：在 101 版（PHP8 兼容版）中，each() 已被注释掉，证明这是一个已知需要修复的问题。在 100 版（当前项目）中需仔细检查 doiconv.php 中的 each() 调用。

---

#### 6. preg_replace /e 修饰符替换

**问题**：`/e` 修饰符在 PHP 7.2+ 中已移除，使用会导致 Fatal Error。

**重点文件**：`e/class/SendEmail.inc.php`（约 2 处，第 1244、1247 行）

**修复模式**

```php
//  修改前
$encoded = preg_replace("/([\001-\010\013\014\016-\037\075\177-\377])/e", 'sprintf("=%02X", ord("\\1"))', $encoded);

//  修改后
$encoded = preg_replace_callback(
    "/([\001-\010\013\014\016-\037\075\177-\377])/",
    function($m) { return '=' . sprintf('%02X', ord($m[1])); },
    $encoded
);
```

---

### P1：严重警告 - 建议尽快修复（导致功能异常）

#### 7. create_function() 替换为匿名闭包

**问题**：`create_function()` 在 PHP 7.2 中已弃用，在 PHP 8 中完全移除。帝国CMS 的模板解析器、灵动标签中大量使用此函数。

**重点文件**：

- `e/class/functions.php`（ReplaceListVars、DoTempletTag 等函数）
- `e/class/t_functions.php`
- `e/class/q_functions.php`

**修复模式**

```php
//  修改前
$callback = create_function('$matches', 'return strtoupper($matches[1]);');

//  修改后
$callback = function($matches) { return strtoupper($matches[1]); };
```

**注意事项**：create_function 的第二个参数是字符串形式的代码体，转换为闭包时要注意变量作用域。如果原代码使用了 `global` 关键字，闭包中需要用 `use()` 引入外部变量。

---

#### 8. split() 函数移除

**问题**：`split()` 基于正则分割字符串，在 PHP 7.0 中已移除，PHP 8 中调用直接 Fatal Error。

**修复模式**

```php
//  修改前
$arr = split(',', $str);
$arr = split('[,;|]', $str);  // 正则分隔

//  修改后（固定分隔符用 explode，性能更好）
$arr = explode(',', $str);

//  修改后（需要正则分隔用 preg_split）
$arr = preg_split('/[,;|]/', $str);
```

---

#### 9. getcvar() 等函数增加 isset() 检查

**问题**：PHP 8 对未定义变量访问的警告级别提升，直接访问 `$_COOKIE[$tvar]` 在 cookie 不存在时会产生 Warning。

**重点文件**：`e/class/connect.php`（第 261 行附近的 getcvar 函数）

**修复模式**

```php
//  修改前
function getcvar($var, $ecms = 0) {
    global $ecms_config;
    $tvar = empty($ecms) ? $ecms_config['cks']['ckvarpre'] . $var : $ecms_config['cks']['ckadminvarpre'] . $var;
    return $_COOKIE[$tvar];  // 无检查，可能产生 PHP 8 Warning
}

//  修改后
function getcvar($var, $ecms = 0) {
    global $ecms_config;
    $tvar = empty($ecms) ? $ecms_config['cks']['ckvarpre'] . $var : $ecms_config['cks']['ckadminvarpre'] . $var;
    if (isset($_COOKIE[$tvar])) return $_COOKIE[$tvar];
    return null;
}
```

---

### P2：兼容性优化 - 建议修复（避免边缘情况异常）

#### 10. 字符串与数字比较行为变更

**问题**：PHP 8 改变了非严格比较规则。`0 == "foo"` 在 PHP 7 中为 true，在 PHP 8 中为 false。帝国CMS 大量使用 `$classid == 0`、`$id != ""` 等宽松比较来判断栏目ID或内容ID。

**后果**：当变量为空字符串 `""` 或 `"0"` 时，条件判断结果反转，导致栏目导航丢失、分页失效或权限校验绕过。

**修复模式**

```php
//  修改前（PHP 8 中结果可能反转）
if ($classid == 0) { ... }
if ($id != "") { ... }

//  修改后（强制转型后严格比较）
if ((int)$classid === 0) { ... }
if ($id !== '') { ... }
```

**检查提示**：搜索项目中的 `== 0`、`!= ""`、`== ""` 模式，尤其在栏目管理、内容列表、权限判断等核心逻辑中。

---

#### 11. implode() 参数顺序

**问题**：`implode($pieces, $glue)` 反向调用在 PHP 8 中已移除，直接抛出 Fatal Error。

**修复模式**

```php
//  修改前（PHP 8 不支持）
$str = implode($array, ',');

//  修改后（glue 在前，pieces 在后）
$str = implode(',', $array);
```

**检查提示**：搜索 `implode($` 并检查参数顺序是否正确。

---

#### 12. PHP 4 风格构造函数

**问题**：类名与方法名相同的构造函数（PHP 4 风格）在 PHP 8.1+ 中已弃用。

**重点文件**：`e/class/SendEmail.inc.php`、`e/class/doiconv.php`、`e/class/ftp.php`、`e/class/phpzip.inc.php`

**修复模式**

```php
//  修改前（PHP 4 风格）
class SendEmail {
    function SendEmail() {  // 类名与方法名相同
        // 构造逻辑
    }
}

//  修改后（PHP 8 风格）
class SendEmail {
    function __construct() {  // 使用 __construct 魔术方法
        // 构造逻辑
    }
}
```

---

#### 13. GBK 编码环境 mbstring 兼容

**问题**：PHP 8 移除了 `mbstring.func_overload` 配置项。若服务器原先依赖该配置实现 GBK 站点中文处理，升级后会出现乱码或截取异常。帝国CMS 7.5 GBK 版受影响尤为严重。

**修复模式**

```php
//  确认所有 mb_substr/mb_strlen 调用显式传入 'GBK' 编码参数
$text = mb_substr($text, 0, 100, 'GBK');
$len = mb_strlen($text, 'GBK');

// UTF-8 版站点可忽略此项
```

---

---

##  目录结构差异：e/action vs e/article

**关键差异**：

| 版本                       | 目录名       | 说明                  |
| -------------------------- | ------------ | --------------------- |
| 101版（PHP8 兼容原版）     | `e/action/`  | 官方标准目录          |
| 100版（PHP7.4 二次开发版） | `e/article/` |  二次开发重命名目录 |

**重要提示**：

1. `e/article/` 目录是 **100 版独有** 的，对应原版的 `e/action/` 目录
2. 升级 PHP 8 时需**单独检查** `e/article/` 目录下的所有文件
3. 不能直接参考原版 `e/action/` 目录中的文件内容（因为二次开发可能有定制逻辑）

**需要检查的文件清单**：

```
e/article/
├── ListInfo.php       (栏目列表)
├── ShowInfo.php       (内容展示)
├── list.php           ( 自定义分页，独有文件)
├── show.php           ( 自定义 404 处理，独有文件)
├── InfoType/
│   └── index.php      (信息类型)
├── ListInfo/
│   └── index.php      (列表)
└── ShowInfo/
    └── index.php      (展示)
```

---

### 独有文件深度分析：e/article/list.php

**文件特征**：自定义分页逻辑 + 随机查询优化 + 伪静态分页处理

**PHP 8 兼容性检查结果**：

| 检查项          | 状态        | 说明                                 |
| --------------- | ----------- | ------------------------------------ |
| 数组键加引号    |  基本完成 | 二次开发代码质量较好，大部分已加引号 |
| SQL 花括号语法  |  正确使用 | `{$dbtbpre}ecms_` 正确使用           |
| count() 调用    |  需检查   | 需确认是否有对不确定变量的 count()   |
| preg_replace /e |  未发现   | 无                                   |
| each()          |  未发现   | 无                                   |
| create_function |  未发现   | 无                                   |
| 自定义分页函数  |  正常     | `MX_ListPage()` 语法兼容             |

**需特别检查的代码段**：

```php
// 第 236 行 - 正则替换（检查是否有 /e 修饰符）
$url = preg_replace('/_[0-9]+/', '', $_SERVER['HTTP_X_REWRITE_URL'] ? $_SERVER['HTTP_X_REWRITE_URL'] : $_SERVER['REQUEST_URI']);
//  无 /e 修饰符，PHP 8 兼容

// 第 214 行 - 随机查询优化（检查 SQL 语法）
$query = "select * from {$dbtbpre}ecms_" . $tbname . " as t1 join (select ROUND(RAND() * ((select MAX(id) from {$dbtbpre}ecms_" . $tbname . ")-(select MIN(id) from {$dbtbpre}ecms_" . $tbname . "))+(select MIN(id) from {$dbtbpre}ecms_" . $tbname . ")) as id) as t2 WHERE t1.id >= t2.id ORDER BY t1.id LIMIT " . $offset . "," . $line . " ";
//  SQL 语法正常（但注意此处使用了 . 连接字符串而非直接在双引号中嵌入数组键，是安全的）
```

**结论**：list.php 的 PHP 8 兼容性较好，主要工作是检查是否有遗漏的未加引号数组键和 count() 调用。

---

### 独有文件深度分析：e/article/show.php

**文件特征**：自定义 404 处理 + 自定义分页 + 强制索引优化 + 模板变量替换

**PHP 8 兼容性检查结果**：

| 检查项          | 状态      | 说明                               |
| --------------- | --------- | ---------------------------------- |
| 数组键加引号    |  有遗漏 | SQL 字符串中和部分数组访问未加引号 |
| SQL 花括号语法  |  有问题 | 第 94、136、204、374、386 行需修复 |
| count() 调用    |  需替换 | 第 225、234、255、296 行           |
| preg_replace /e |  未发现 | 无                                 |
| each()          |  未发现 | 无                                 |
| create_function |  未发现 | 无                                 |

**具体需修复的代码段**：

```php
// ============================================================
// 1. SQL 语句中的未加引号数组键（第 94 行）
// ============================================================
//  修改前
$finfor = $empire->fetch1("select " . ReturnSqlFtextF($mid) . " from {$dbtbpre}ecms_" . $tbname . "_data_" . $r['stb'] . " where id='$r[id]' limit 1");
//                                                                                                         ^^^^^ 未加引号

//  修改后
$finfor = $empire->fetch1("select " . ReturnSqlFtextF($mid) . " from {$dbtbpre}ecms_" . $tbname . "_data_" . $r['stb'] . " where id={$r['id']} limit 1");
//                                                                                                         ^^^^^^^^^ 加引号并使用花括号


// ============================================================
// 2. SQL 语句中的未加引号数组键（第 136 行）
// ============================================================
//  修改前
$newstemp_r = $empire->fetch1("select tempid,temptext,showdate from " . GetTemptb("enewsnewstemp") . " where tempid='$r[newstempid]'");
//                                                                                                      ^^^^^^^^^^^^ 未加引号

//  修改后
$newstemp_r = $empire->fetch1("select tempid,temptext,showdate from " . GetTemptb("enewsnewstemp") . " where tempid={$r['newstempid']}");
//                                                                                                      ^^^^^^^^^^^^^^^^ 加引号并使用花括号


// ============================================================
// 3. SQL 语句中的未加引号数组键（第 204 行）
// ============================================================
//  修改前
$empire->query("update {$dbtbpre}ecms_" . $tbname . " set onclick=onclick+1 where id='$add[id]' limit 1");
//                                                                                       ^^^^^^^ 未加引号

//  修改后
$empire->query("update {$dbtbpre}ecms_" . $tbname . " set onclick=onclick+1 where id={$add['id']} limit 1");
//                                                                                       ^^^^^^^^^^ 加引号并使用花括号


// ============================================================
// 4. count() 调用替换（第 225 行）
// ============================================================
//  修改前
$thispagenum = count($n_r);

//  修改后
$thispagenum = php8_count($n_r);


// ============================================================
// 5. count() 调用替换（第 234、255 行）
// ============================================================
//  修改前
if (count($ti_r) >= 2) { ... }

//  修改后
if (php8_count($ti_r) >= 2) { ... }


// ============================================================
// 6. count() 调用替换（第 296 行）
// ============================================================
//  修改前
$fcount = count($fr) - 1;

//  修改后
$fcount = php8_count($fr) - 1;


// ============================================================
// 7. SQL 语句中的未加引号数组键（第 374、386 行 - 上下篇查询）
// ============================================================
//  修改前
$next_r = $empire->fetch1("select isurl,titleurl,classid,id,title from {$dbtbpre}ecms_" . $class_r[$add['classid']]['tbname'] . " FORCE INDEX (idx_classid_id_asc) where id>$add[id] and classid='$add[classid]' order by id limit 1");
//                                                                                                                                                                       ^^^^^^^          ^^^^^^^^^^^^ 未加引号

//  修改后
$next_r = $empire->fetch1("select isurl,titleurl,classid,id,title from {$dbtbpre}ecms_" . $class_r[$add['classid']]['tbname'] . " FORCE INDEX (idx_classid_id_asc) where id>{$add['id']} and classid={$add['classid']} order by id limit 1");
//                                                                                                                                                                       ^^^^^^^^^^          ^^^^^^^^^^^^^^^^ 加引号并使用花括号

// 第 386 行（上一篇）类似修复
```

**结论**：show.php 需要 5-7 处针对性修复，主要集中在 SQL 语句的数组键引用和 count() 调用上。这是一个典型的"二次开发代码 PHP 8 兼容性问题"模式。

---

##  按目录推进的实操 Checklist

建议从最核心的文件开始，按以下顺序修复，**每完成一个文件测试一次**，避免一次性修改太多导致难以定位问题。

### 第一步：核心基础（完成后，PHP 8 应能启动）

- [ ] **修复 `e/class/connect.php`**
  - [ ] 第 2 行：`error_reporting(E_ALL ^ E_NOTICE ^ E_DEPRECATED);`
  - [ ] 第 7 行：`define('MAGIC_QUOTES_GPC', function_exists('get_magic_quotes_gpc') && get_magic_quotes_gpc());`
  - [ ] 文件末尾：添加 `function php8_count($a) { return is_array($a) ? count($a) : 0; }`

**验证**：访问首页、后台登录页，确认不再白屏（可能还有 Notice/Warning，但不再是 Fatal Error）

---

### 第二步：核心函数库

- [ ] **修复 `e/class/functions.php`**（~1006 处数组键 + ~46 处 count() + 若干 SQL 花括号）
- [ ] **修复 `e/class/classfun.php`**（~1462 处数组键 + ~9 处 count() + 若干 SQL 花括号）
- [ ] **修复 `e/class/hinfofun.php`**（~630 处数组键 + ~17 处 count()）
- [ ] **修复 `e/class/moddofun.php`**（~865 处数组键 + ~24 处 count()）
- [ ] **修复 `e/class/cjfun.php`**（~330 处数组键）
- [ ] **修复 `e/class/t_functions.php`**（~308 处数组键）
- [ ] **修复 `e/class/doiconv.php`**（each() → foreach，约 6 处）
- [ ] **修复 `e/class/SendEmail.inc.php`**（preg_replace /e → preg_replace_callback，2 处）

**验证**：测试后台登录、栏目管理、内容管理、邮件发送等核心功能

---

### 第三步：后台管理（e/admin/ - 最大工作量）

- [ ] **`e/admin/SetEnews.php`**（~640 处数组键）
- [ ] **`e/admin/ListGroup.php`**（~647 处数组键）
- [ ] **`e/admin/AddNews.php`**（count() + 数组键）
- [ ] **`e/admin/ListClass.php`**（数组键）
- [ ] **`e/admin/workflow/ListWfItem.php`**（count() + 数组键）
- [ ] **其他 e/admin/ 下的所有 PHP 文件**（逐文件检查）

**验证**：测试后台所有功能模块

---

### 第四步：二次开发模块（ 重点检查！）

- [ ] **`e/article/` 目录（独有目录！）**
  - [ ] `ListInfo.php`
  - [ ] `ShowInfo.php`
  - [ ] `list.php`（自定义分页）
  - [ ] `show.php`（需修复 5-7 处，详见上文）
  - [ ] `InfoType/index.php`
  - [ ] `ListInfo/index.php`
  - [ ] `ShowInfo/index.php`

- [ ] **`e/dongpo/` 目录（二次开发模块）**（~434 处数组键）
- [ ] **`e/admin/sinfo/` 目录（二次开发模块）**（~277 处数组键）

**验证**：测试前台栏目列表页、内容详情页、404 页面

---

### 第五步：会员系统 & 其他

- [ ] **`e/member/` 目录**（~337 处数组键 + count()）
  - [ ] `class/member_modfun.php`
  - [ ] `list/index.php`
  - [ ] `cp/index.php`
  - [ ] `my/index.php`
- [ ] **`e/template/` 目录**
- [ ] **`e/space/` 目录**
- [ ] **`e/enews/` 目录**
- [ ] **`e/pl/` 目录（如果有）**
- [ ] **`e/public/` 目录（如果有）**

**验证**：测试会员注册、登录、空间访问等功能

---

### 第六步：其他兼容性修复

- [ ] **create_function() 替换**：检查 functions.php、t_functions.php、q_functions.php
- [ ] **split() 替换**：全局搜索 `split(`
- [ ] **implode() 参数顺序**：全局搜索 `implode($`
- [ ] **PHP 4 风格构造函数**：检查 SendEmail.inc.php、ftp.php、phpzip.inc.php
- [ ] **字符串与数字比较**：搜索 `== 0`、`!= ""` 并评估是否需要严格比较
- [ ] **GBK mbstring 兼容**：GBK 版检查 mb_substr/mb_strlen 编码参数

---

##  危险操作警告区

###  绝对禁止批量替换数组键

**风险**：如果使用正则批量替换 `$var[word]` → `$var['word']`，会将变量键名 `$var[$i]` 错误地替换成 `$var['$i']`，导致严重逻辑错误。

**安全操作**：

1. 逐个文件手动修复
2. 使用 IDE 的"查找所有"功能定位，逐一确认后替换
3. 对 `$var[$...]`、`$var[0-9]`、`$var[常量名]` 模式**跳过不替换**

###  禁止直接复制原版文件覆盖

**风险**：101 版（PHP8 兼容版）文件结构与 100 版（二次开发版）可能有差异，直接覆盖会丢失二次开发功能（如 e/article/ 目录的自定义分页、404 处理等）。

**安全操作**：以 100 版文件为基础，参考 101 版的 PHP 8 写法进行修改，**不要直接文件覆盖**。

###  注意 GBK 文件编码

**风险**：项目文件使用 GBK 编码，使用 UTF-8 编辑器保存会导致中文乱码。

**安全操作**：使用支持 GBK 编码的编辑器（如 EditPlus、UltraEdit、VS Code 设置为 GBK 编码）打开和保存文件。

###  备份！备份！备份！

**操作前务必备份**：

1. 备份整个 `e/` 目录
2. 备份数据库
3. 记录下当前 PHP 版本号
4. 确认备份可以恢复后再开始修改

**你的备份目录**：`J:\Vhosts\127.0.2.100\bat_7.5\`（已确认存在，结构与主目录一致）

---

##  常见故障速查表

| 现象                                           | 可能原因                                | 检查文件                                   | 修复方法                                                |
| ---------------------------------------------- | --------------------------------------- | ------------------------------------------ | ------------------------------------------------------- |
| 页面白屏，无任何输出                           | PHP Fatal Error                         | 所有修改过的文件                           | 检查 PHP 错误日志，定位 undefined constant 或 TypeError |
| 页面显示 `Error: Undefined constant "xxx"`     | 数组键未加引号                          | 报错文件对应行                             | 将 `$r[xxx]` 改为 `$r['xxx']`                           |
| 页面显示 `TypeError: count(): Argument #1 ...` | count() 参数非数组                      | 报错文件对应行                             | 将 `count($var)` 改为 `php8_count($var)`                |
| 邮件发送失败                                   | preg_replace /e 未修复                  | `e/class/SendEmail.inc.php`                | 替换为 preg_replace_callback                            |
| 栏目导航丢失                                   | 字符串与数字比较结果反转                | 栏目相关 PHP 文件                          | 将 `$classid == 0` 改为 `(int)$classid === 0`           |
| 中文乱码                                       | 文件编码损坏或 mbstring 配置变化        | GBK 版所有文件                             | 检查文件编码，确保 mbstring 函数显式传入编码参数        |
| 分页异常                                       | show.php/list.php count() 或 SQL 未修复 | `e/article/show.php`、`e/article/list.php` | 修复 count() 和 SQL 花括号语法                          |
| 模板标签不生效                                 | create_function 未替换                  | `e/class/functions.php`、t_functions.php   | 将 create_function 替换为匿名闭包                       |

---

##  验证测试清单

完成所有修改后，按以下顺序进行验证测试：

### 基础功能测试

- [ ] 首页正常打开（无白屏、无 Fatal Error）
- [ ] 后台登录页正常
- [ ] 后台登录成功
- [ ] 退出登录正常

### 栏目 & 内容测试

- [ ] 栏目列表页正常（e/article/ 自定义目录）
- [ ] 内容详情页正常
- [ ] 内容分页正常（show.php 自定义分页）
- [ ] 上一篇/下一篇正常（show.php 强制索引查询）
- [ ] 404 页面正常（show.php 自定义 404 处理）

### 后台管理测试

- [ ] 栏目管理（新增、修改、删除）
- [ ] 内容管理（新增、修改、删除）
- [ ] 模板管理
- [ ] 会员管理

### 会员功能测试

- [ ] 会员注册
- [ ] 会员登录
- [ ] 会员空间访问

### 邮件 & 其他功能测试

- [ ] 邮件发送正常（找回密码、通知邮件）
- [ ] 文件上传正常
- [ ] 图片处理正常
- [ ] 搜索功能正常

---

##  修改记录表（模板）

建议在升级过程中维护一个修改记录表：

| 日期       | 文件                    | 修改内容                                                | 修改量   | 完成人 | 验证状态  |
| ---------- | ----------------------- | ------------------------------------------------------- | -------- | ------ | --------- |
| 2026-xx-xx | `e/class/connect.php`   | 修复 error_reporting、MAGIC_QUOTES_GPC、添加 php8_count | 3 处     |        |  已验证 |
| 2026-xx-xx | `e/class/functions.php` | 数组键加引号 + count() 替换 + SQL 花括号                | ~1050 处 |        |  已验证 |
| 2026-xx-xx | `e/article/show.php`    | 修复 SQL 数组键 + count()                               | 5-7 处   |        |  已验证 |
| ...        | ...                     | ...                                                     | ...      |        | ...       |

---

##  参考对比

以下是 101 版（PHP8 兼容原版）与 100 版（PHP7.4 二次开发版）的典型代码对比，可作为修复时的参考模式：

### 模式 1：简单数组键

```php
// 100版（PHP7.4）
$r[wburl]
$r[newstime]
$r[classid]
$r[id]
$public_r[newsurl]

// 101版（PHP8）
$r['wburl']
$r['newstime']
$r['classid']
$r['id']
$public_r['newsurl']
```

### 模式 2：多维数组（最常见）

```php
// 100版（PHP7.4）
$class_r[$classid][tbname]
$class_r[$classid][modid]
$class_r[$classid][islast]
$ecms_tofunr[cacheuse]
$emod_r[$mid][tempf]

// 101版（PHP8）
$class_r[$classid]['tbname']      // 注意：$classid 是变量，不加引号！
$class_r[$classid]['modid']
$class_r[$classid]['islast']
$ecms_tofunr['cacheuse']
$emod_r[$mid]['tempf']
```

### 模式 3：count() 调用

```php
// 100版（PHP7.4）
$count = count($r) - 1;
for ($i = 0; $i < count($myorder); $i++) { ... }

// 101版（PHP8）
$count = php8_count($r) - 1;
for ($i = 0; $i < php8_count($myorder); $i++) { ... }
```

### 模式 4：SQL 语句

```php
// 100版（PHP7.4）
$empire->query("select ... where classid='$r[classid]' and id='$r[id]'");

// 101版（PHP8）
$empire->query("select ... where classid={$r['classid']} and id={$r['id']}");
```

---

_最后更新：基于 127.0.2.100（PHP7.4 二次开发版）与 127.0.2.101（PHP8 兼容原版）的差异对比_
