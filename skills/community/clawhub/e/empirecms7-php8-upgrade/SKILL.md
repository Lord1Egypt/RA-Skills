---
name: "empirecms7.5-php8-upgrade"
description: "帝国CMS 7.5 升级到 PHP 8 兼容性修改完整清单。当用户需要将帝国CMS 7.5 升级到 PHP 8、修复 PHP 8 致命错误、或从 PHP 7.x 迁移到 PHP 8 时调用。"
---

# 帝国CMS 7.5 PHP 8 兼容性升级技能（完整版）

本技能提供帝国CMS 7.5 升级到完全兼容 PHP 8.x 的完整方法论。基于对可运行 PHP 8 兼容版本的逆向分析总结，覆盖语法兼容、语义兼容及运行时环境适配。

## 何时调用

- 用户需要将帝国CMS 7.5 升级到 PHP 8
- 用户报告 PHP 8 致命错误（白屏、TypeError、Fatal Error 等）
- 用户需要修复帝国CMS的 PHP 8 兼容性问题
- 用户询问 php8_count、get_magic_quotes_gpc、preg_replace /e、create_function、split、字符串比较异常等问题

## 核心修改方法（15 大类，按优先级排序）

### 1. 数组键加引号（P0 致命错误 - PHP 8 基础规范，最关键）

问题：未加引号的数组键如 `$var[key]` 在 PHP 8 中会被当作常量解析，常量未定义时抛出 `Error: Undefined constant "key"` 致命错误。这是 PHP 8 兼容的**基础规范**，修改量最大（11,000+ 处），遍布 200+ 个文件。

严重程度对比：

- PHP 7.x：视为未定义常量，回退为字符串 `'key'`（仅警告）
- PHP 8.0+：抛出 `Error: Undefined constant "key"`（致命错误，白屏）

#### 加引号的原则（必须遵守）

**必须加引号的情况**（字符串字面量键名）：

    // 原代码（PHP 8 致命错误）→ 修复后（PHP 8 兼容）
    $r[myorder]=0;                    → $r['myorder']=0;
    $r[listorder]="id DESC";          → $r['listorder']="id DESC";
    $_GET[classid]                    → $_GET['classid']
    $_POST[from]                      → $_POST['from']
    $class_r[$classid][featherclass]  → $class_r[$classid]['featherclass']

**不需要加引号的情况**（切勿误改）：

    // 1. 变量键名 - 不加引号
    $r[$key]                // ✅ 正确（变量作为键名）
    $r[$classid]            // ✅ 正确
    $r[$i]                  // ✅ 正确

    // 2. 数字索引 - 不加引号
    $r[0]                   // ✅ 正确
    $arr[1]                 // ✅ 正确
    $r[$i+1]                // ✅ 正确（表达式）

    // 3. 已加引号的 - 不修改
    $r['key']               // ✅ 已正确
    $r["key"]               // ✅ 已正确

    // 4. 已定义常量键名 - 不加引号
    define('MY_CONST', 'value');
    $r[MY_CONST]            // ✅ 正确（是常量，不是字符串）

**特殊情况（双引号字符串内）**：

    "$r[key]"               // ⚠️ PHP 7/8 都合法（先查常量，回退字符串）
    "{$r['key']}"           // ✅ 推荐写法（花括号语法）

#### 判断流程

遇到 `$var[key]` 时按以下顺序判断：

1. key 是变量（$key）？ → **不加引号**
2. key 是数字（0）？ → **不加引号**
3. key 是表达式（$i+1）？ → **不加引号**
4. key 是已定义常量（MY_CONST）？ → **不加引号**
5. key 已加引号（'key'）？ → **不修改**
6. key 是字符串字面量（myorder）？ → ✅ **加引号**

#### 应用范围与统计

**全项目所有 PHP 文件**，重点文件：

- e/class/\*.php（connect.php 162处、functions.php 1006处、hinfofun.php 630处、classfun.php 1462处、moddofun.php 865处、cjfun.php 330处、t_functions.php 308处等）
- e/admin/\*.php 及其子目录（SetEnews.php 640处、ListGroup.php 647处、ListAd.php 192处、AddClass.php 180处等）
- e/member/\*.php（337处）
- e/dongpo/\*.php（434处，二次开发模块）
- e/sinfo/\*.php（277处，二次开发模块）
- e/action/\*.php（127处）

修改统计：**11,101+ 处**（基于 Grep 搜索 `\$\w+\[[a-zA-Z_]\w*\]` 模式统计）

#### 注意事项

1. **切勿批量替换**：必须逐个判断是否为字符串字面量，避免误改变量键名和常量键名
2. **双引号字符串内**：`"$var[key]"` 在 PHP 8 中仍合法，但建议改为 `"{$var['key']}"`
3. **多维数组**：只加字符串字面量的键名，如 `$class_r[$classid]['featherclass']`（$classid 是变量不加，featherclass 是字符串要加）
4. **编码注意**：修改时保持文件原有编码（GBK/UTF-8），避免中文注释乱码

#### SQL 语句中的数组键花括号语法（重要子类）

问题：在 SQL 语句（双引号字符串）中直接嵌入数组键时，`'$var[key]'` 在 PHP 8 中会触发未定义常量错误。

解决方案：使用花括号语法 `{$var['key']}`：

    // 原代码（PHP 8 致命错误）
    $sql = "... where bid='$cr[bid]'";
    $sql = "... bname='$add[bname]'";
    $sql = "... where userid='$user_r[userid]'";

    // 修复后（PHP 8 兼容）
    $sql = "... where bid='{$cr['bid']}'";
    $sql = "... bname='{$add['bname']}'";
    $sql = "... where userid='{$user_r['userid']}'";

判断流程：

1. 在双引号字符串中看到 `$var[key]` → 必须改为 `{$var['key']}`
2. 在 SQL 语句中看到 `'$var[key]'` → 必须改为 `'{$var['key']}'`
3. 注意：`$var[$key]`（变量键名）在双引号字符串中也需要花括号：`{$var[$key]}`

### 2. php8_count() 包装函数（P0 致命错误）

问题：PHP 8 中 count() 对 null/非数组参数抛出 TypeError。

解决方案：在 e/class/connect.php 末尾（?> 之前）添加包装函数：

    //为了count for php8
    function php8_count($a){
        return is_array($a) ? count($a) : 0;
    }

应用范围：将以下文件中的 count($var) 替换为 php8_count($var)：

    e/class/*.php（functions.php、connect.php、hinfofun.php、com_functions.php 等）
    e/admin/*.php 及其子目录
    e/member/*.php
    e/action/*.php
    e/pl/*.php、e/search/*.php、e/ShopSys/*.php 等

修改统计：约 363 处调用（connect.php 29处、functions.php 46处、hinfofun.php 17处、com_functions.php 13处、cjfun.php 30处、tempfun.php 16处、moddofun.php 24处、classfun.php 9处、memberfun.php 7处、hplfun.php 7处等）

例外与性能注意：当变量确定是数组时保留原生 count()（如 count(array(1,2,3)) 或数据库结果集）。仅在变量来源不确定时使用 php8_count()，避免高频循环中的性能损耗。

### 3. isset() 未定义变量检查（P1 警告 - 安全模式）

问题：PHP 8 对未定义变量访问抛出 Warning，且在 isset() 之前直接访问变量名本身也可能触发警告。

解决方案：优先在函数签名中设置默认值，而非在函数体内赋值：

    // 推荐：函数签名默认值
    function RepClassid($classid = null) { ... }

    // 备选：仅当无法修改签名时使用 func_get_arg
    $classid = func_num_args() > 0 ? func_get_arg(0) : null

修改统计：约 944 处（e/admin/ 616处、e/class/ 248处、e/member/ 22处、e/ShopSys/ 6处等）

应用范围：e/class/_.php、e/admin/_.php、e/member/_.php、e/ShopSys/_.php 中使用 $classid 等未初始化变量的函数。

### 4. magic_quotes_gpc 兼容性（P0 致命错误）

问题：get_magic_quotes_gpc() 在 PHP 8 中已移除。

解决方案：在 e/class/connect.php 中：

    define('MAGIC_QUOTES_GPC', function_exists('get_magic_quotes_gpc') && get_magic_quotes_gpc());

### 4. error_reporting 调整

问题：PHP 8 弃用警告会破坏输出。

解决方案：在 e/class/connect.php 中：

    // 文件顶部
    error_reporting(E_ALL ^ E_NOTICE ^ E_DEPRECATED);

    // 后台页面
    error_reporting(E_ALL & ~E_WARNING & ~E_DEPRECATED & ~E_USER_DEPRECATED);

### 5. preg_replace_callback() 替代 /e 修饰符

问题：/e 修饰符在 PHP 7.2+ 中已移除。

解决方案：在 e/class/SendEmail.inc.php 和 e/class/connect.php 中：

    $encoded = preg_replace_callback(
        "/([\001-\010\013\014\016-\037\075\177-\377])/",
        function($m) { return '='.sprintf('%02X', ord($m[1])); },
        $encoded
    );

特别注意：SendEmail.inc.php 第 1244、1247 行的 /e 修饰符必须手动确认修复状态。若未修复，邮件编码功能将完全不可用并抛出致命错误。

### 6. each() 改为 foreach

问题：each() 在 PHP 8 中已移除。

解决方案：在 e/class/doiconv.php、e/install/data/fun.php 中：

    foreach($tmp as $key => $value) { ... }

### 7. 类构造函数 \_\_construct()

问题：PHP 4 风格构造函数（方法名=类名）已弃用。

解决方案：在 e/class/SendEmail.inc.php、e/class/doiconv.php 中将同名方法改为 \_\_construct()。

### 8. mysql*\* 改为 mysqli*\*

问题：mysql\_\* 扩展在 PHP 7+ 中已移除。

解决方案：

    设置 e/config/config.php：$ecms_config['db']['usedb'] = 'mysqli';
    如果 e/class/db/db_mysql.php 被加载，将所有 mysql_* 转换为 mysqli_*
    注意参数顺序不同：mysql_query($sql, $link) 改为 mysqli_query($link, $sql)

### 9. PHP 4 风格 var $ 属性声明

问题：var $ 属性声明在 PHP 8.1+ 中已弃用。

解决方案：在 e/class/ftp.php、e/class/phpzip.inc.php 中：

    class ftp {
        public $ftpconnectid;
        public $ftptranmode;
    }

### 11. 字符串与数字比较行为变更（高危语义陷阱）

问题：PHP 8 改变了非严格比较规则。0 == "foo" 在 PHP 7 中为 true，在 PHP 8 中为 false。帝国CMS 大量使用 $classid == 0、$id != "" 等宽松比较来判断栏目ID或内容ID。

后果：当变量为空字符串 "" 或 "0" 时，条件判断结果反转，导致栏目导航丢失、分页失效或权限校验绕过。

解决方案：将关键业务逻辑中的 == / != 改为 === / !==，或对 $classid、$id 等核心变量强制 (int) 转型后再比较：

    // 推荐：强制转型后严格比较
    if ((int)$classid === 0) { ... }

    // 推荐：严格不等于
    if ($id !== '') { ... }

### 12. implode() 参数顺序与 create_function() 移除

问题A：implode($pieces, $glue) 反向调用在 PHP 8 中已移除，直接抛出 Fatal Error。

问题B：create_function() 在 PHP 8 中完全移除，影响模板解析引擎和自定义标签处理。

解决方案：

    // implode 修复：确保 glue 在前
    $str = implode(',', $array);

    // create_function 修复：替换为闭包
    // 原代码
    $callback = create_function('$matches', 'return strtoupper($matches[1]);');
    // 修复后
    $callback = function($matches) { return strtoupper($matches[1]); };

### 13. split() 函数移除（新增遗漏项）

问题：split() 基于正则分割字符串，在 PHP 7.0 中已移除，PHP 8 中调用直接 Fatal Error。帝国CMS 部分旧版插件和自定义标签中仍在使用。

解决方案：统一替换为 explode()（按固定分隔符）或 preg_split()（按正则）：

    // 原代码
    $arr = split(',', $str);
    // 修复后（固定分隔符用 explode）
    $arr = explode(',', $str);

    // 原代码（正则分隔）
    $arr = split('[,;|]', $str);
    // 修复后
    $arr = preg_split('/[,;|]/', $str);

### 14. GBK 编码环境 mbstring 兼容（新增遗漏项）

问题：PHP 8 移除了 mbstring.func_overload 配置项。若服务器原先依赖该配置实现 GBK 站点中文处理，升级后会出现乱码或截取异常。帝国CMS 7.5 GBK 版受影响尤为严重。

解决方案：

    确认 e/class/connect.php 中所有字符串操作使用 mb_substr/mb_strlen 时显式传入 'GBK' 编码参数
    不再依赖 mbstring.func_overload 自动重载
    UTF-8 版站点可忽略此项

### 15. 模板标签解析引擎适配（新增遗漏项）

问题：帝国CMS 的灵动标签、万能标签解析器内部使用 create_function() 动态生成回调，是第 12 条的特化场景。仅替换通用 create_function 可能遗漏标签解析器中的嵌套调用。

解决方案：重点检查以下文件中的 create_function 调用：

    e/class/functions.php（ReplaceListVars、DoTempletTag 等函数）
    e/class/t_functions.php
    e/class/q_functions.php

    将每个 create_function 逐一替换为匿名闭包，注意保持参数列表和返回值语义一致。

## 执行步骤

### 第一步：备份

    xcopy /E /I /Y "项目目录" "项目目录_php8备份"

### 第二步：添加核心兼容函数

编辑 e/class/connect.php：

- 在文件末尾添加 php8_count() 函数
- 修复 MAGIC_QUOTES_GPC 定义
- 调整文件顶部的 error_reporting
- 将 preg_replace /e 替换为 preg_replace_callback

### 第三步：应用 php8_count() 替换

对项目中的所有目标文件执行批量替换，将 count($var) 替换为 php8_count($var)，注意保留确定数组类型的原生 count() 调用。

### 第四步：修复未定义变量

逐一检查 e/class、e/admin、e/member 目录下的函数，为缺少默认值的参数添加 null 默认值或使用 func_get_arg 兜底。

### 第五步：修复数组键引号

使用正则搜索 \$_(GET|POST|REQUEST|SESSION|COOKIE)\[[a-zA-Z_]+\] 和 \$class*r\[.\*?\]\[[a-zA-Z*]+\]，为裸键名添加单引号。

### 第六步：修复 create_function 与 split

全局搜索 create_function 和 split(，按第 12、13、15 条逐一替换为闭包和 explode/preg_split。

### 第七步：验证与测试

- 开启 error_reporting(E_ALL) 进行全量扫描
- 重点测试后台登录、栏目管理、内容发布、前台首页、搜索、评论、会员系统
- 确认邮件发送功能正常（SendEmail.inc.php）
- 确认 FTP 上传和 ZIP 解压功能正常
- 确认灵动标签、万能标签在前台正常渲染（模板解析引擎）
- GBK 站点额外测试中文标题截取、搜索关键词高亮是否正常
