## 语法支持

BLS 支持基础的 SELECT 查询，具体查询语法是

```SQL
SELECT
    select_expr [, select_expr] ...
    [FROM subquery [AS] table_id]
    [WHERE where_condition]
    [GROUP BY {col_name | expr}, ... ]
    [HAVING where_condition]
    [ORDER BY {col_name | expr} [ASC | DESC], ...]
    [LIMIT [offset,] row_count]
```
其中，where_condition 是一个执行结果为布尔值的条件表达式。不需要子查询的时候不写 FROM 子句。

字段名**大小写敏感**，且尽量避免使用[关键字](#关键字)，如果使用了关键字要加反引号，例如：\`action\`。


## 运算符

**一元前缀运算**

|操作符|示例|描述|
|:--|:--|:--|
|+/-|-A|改变参数的符号|

**二元运算**

|操作符|示例|描述|
|:--|:--|:--|
|+|A + B|加法运算|
|-|A - B|减法运算|
|\*|A \* B|乘法运算|
|/|A / B|除法运算|
|%|A % B|模数运算，结果是 A 除以 B 的余数|
|->|column->path|json_extract()的简写，从指定列的JSON字符串中提取指定path的内容，例如 json->"$.b"|

**关系运算**

|操作符|示例|描述|
|:--|:--|:--|
|=|A = B|如果 A 等于 B，返回 TRUE，否则返回 FALSE。如果 A 与 B 的类型不可比较，返回 NULL|
|!=|A != B|如果 A 不等于 B，返回 TRUE，否则返回 FALSE。如果 A 与 B 的类型不可比较，返回 NULL|
|>|A > B|如果 A 大于 B，返回 TRUE，否则返回 FALSE。如果 A 与 B 的类型不可比较，返回 NULL|
|>=|A >= B|如果 A 大于等于 B，返回 TRUE，否则返回 FALSE。如果 A 与 B 的类型不可比较，返回 NULL|
|<|A < B|如果 A 小于 B，返回 TRUE，否则返回 FALSE。如果 A 与 B 的类型不可比较，返回 NULL|
|<=|A <= B|如果 A 小于等于 B，返回 TRUE，否则返回 FALSE。如果 A 与 B 的类型不可比较，返回 NULL|
|\[NOT\] LIKE|A LIKE pattern|如果 A \[不\]符合 pattern，返回 TRUE，否则返回 FALSE|
|IS \[NOT\] NULL|A IS NULL|如果 A \[不\]为 NULL，返回 TRUE，否则返回 FALSE|
|IS \[NOT\] TRUE/FALSE|A IS TRUE|如果 A \[不\]为 TRUE/FALSE，返回 TRUE，否则返回 FALSE|
|BETWEEN|EXPR BETWEEB A AND B|如果表达式 EXPR 的值大于等于 A 且小于等于 B，则返回 TRUE，否则返回 FALSE，等价于  EXPRESSION >= A AND EXPRESSION <= B|

**逻辑运算**

|操作符|示例|描述|
|:--|:--|:--|
|\[NOT\] IN|A IN (val1, val2, ...)|如果 A \[不\]等于 任何一个参数值，返回 TRUE，否则返回 FALSE|
|AND|A AND B|如果 A 和 B 都为 TRUE，返回 TRUE，否则返回 FALSE。如果 A 或 B 不是布尔类型，返回 NULL|
|OR|A OR B|如果 A 或 B 为 TRUE，返回 TRUE，否则返回 FALSE。如果 A 或 B 不是布尔类型，返回 NULL|
|NOT|NOT A|如果 A 为 FALSE，返回 TRUE，否则返回 FALSE。如果 A 不是布尔类型，返回 NULL|


## 内置函数

### 类型转换函数

|函数签名|返回值|描述|示例|
|:--|:--|:--|:--|
|cast(expr as <type\>)|<type\>|将 expr 的值转换成 <type\> 类型，<type\> 支持 BIGINT, DECIMAL, VARCHAR, TIMESTAMP|>select cast("123" as BIGINT)<br />123|

### 聚合函数

|函数签名|返回值|描述|示例|
|:--|:--|:--|:--|
| count(\*),count(expr),count(DISTINCT expr) | Int    | 统计日志条数                                 | >select count(\*)<br />10                     |
| count_if(expr)                             | Int    | 统计满足指定条件的日志条数。                       | >select count_if(num > 0)<br />10             |
| sum(col)                                   | T      | 计算元素的和                                           | >select sum(num)<br />983                     |
| avg(col)                                   | Double | 计算元素的平均值                                       | >select avg(num)<br />73.14                   |
| max(col)                                   | T      | 计算元素的最大值                                       | >select max(num)<br />99                      |
| min(col)                                   | T      | 计算元素的最小值                                       | >select min(num)<br />62                      |
| first(col)                                 | T      | 计算元素的首个值                                       | >select first(num)<br />87                    |
| last(col)                                  | T      | 计算元素的最后一个值                                   | >select last(num)<br />95                     |
| arbitrary(col)                             | T      | 返回任意一个非空的值                                         | >select arbitrary(num)<br />21                      |
| bitwise_and_agg(col)                       | Int    | 返回所有值按位与运算（AND）的结果                      | >select bitwise_and_agg(num)<br />1024        |
| bitwise_or_agg(col)                        | Int    | 返回所有值按位或运算（OR）的结果                       | >select bitwise_and_agg(num)<br />2047        |
| bool_and(col)                              | Bool   | 判断是组内是否所有表达式都满足条件。如果是，则返回true | >select bool_and(result)<br />true            |
| bool_or(col)                               | Bool   | 判断是组内是否存在表达式都满足条件。如果是，则返回true | >select bool_and(result)<br />false           |
| checksum(col)                              | String | 计算组内元素的校验和，以base64的编码形式输出           | >select checksum(x)<br />dGhpcyBpcyBhIHRlc3Q= |
| max_by(x, y)                               | T      | 查询当y为最大值时对应的x值                             | >select max_by(x,y)<br />32                   |
| min_by(x,y)                                | T      | 查询当y为最小值时对应的x值                             | >select min_by(x,y)<br />42                   |
| percentile_rank(KEY,value...)                                | Float/Array<Float \>      | 查询当KEY为value值时对应的百分位值，value可以是多个，多个value返回多个百分位值                             | >select percentile_rank(latency,0.1)<br />0.95                   |

### 字符串函数

|函数签名|返回值|描述|示例|
|:--|:--|:--|:--|
|reverse(String str)|String|返回反向顺序的字符串|>select reverse("hello")<br />olleh|
|lower(String str)|String|返回小写格式字符串|>select lower("fOoBaR")<br />foobar|
|upper(String str)|String|返回大写格式字符串|>select upper("fOoBaR")<br />FOOBAR|
|capitalize(String str)|String|返回所有单词首字母大写格式的字符串|>select capitalize("fOoBaR")<br />FOoBaR|
|substring(String str, Int start \[, Int len\])|String|返回原字符串从 start 位置开始，长度为 len 的子串。start 从 1 开始，支持负数，此时从结尾开始反向计算位置。len 参数不传表示截取到字符串结尾|>select substring("fOoBaR", 2, 4)<br />OoBa<br />>select substring("fOoBaR", -3, 2)<br />Ba|
|substr(String str,  Int start \[, Int len\])|String|substring() 的别名|select substr("fOoBaR", 2, 4)<br />OoBa<br />>select substr("fOoBaR", -3, 2)<br />Ba|
|replace(String str, String OLD, String NEW)|String|返回 OLD 子串被替换为 NEW 子串的字符串 str|>select replace("abcdef", "abc", "cba")<br />cbadef|
|length(String str)|Int|返回字符串的长度|>select length("abcdef")<br />6|
|chr(Int x)|String|返回ASCII码对应的字母|>select chr(99)<br />c|
|codepoint(char x)|Int|返回字符对应的ASCII码|>select codepoint('c')<br />99|
|levenshtein_distance(String x, String y)|Int|返回x与y之间的最小编辑距离|>select levenshtein_distance('cg', 'cdefg')<br />3|
|lpad(String x, Int length, String lpad_string)|String|在字符串的开头填充指定字符，直到指定长度后返回结果字符串|>select lpad('qqq',10,'p')<br />pppppppqqq|
|rpad(String x, Int length, String lpad_string)|String|在字符串的尾部填充指定字符，直到指定长度后返回结果字符串|>select rpad('qqq',10,'p')<br />qqqppppppp|
|ltrim(String x)|String|删除字符串中开头的空格|>select ltrim(' dhsk') <br />dhsk|
|rtrim(String x)|String|删除字符串结尾的空格|>select rtrim('dhsk ') <br />dhsk|
|trim(String x)|String|删除字符串中开头和结尾的空格|>select trim(' dhsk ') <br />dhsk|
|normalize(String x)|String|返回NFC格式化的字符串|>select normalize('schön')<br />schön|
|strpos(String x, String sub_string)|Int|返回目标子串在字符串中的位置|>select strpos('china news','news') <br />7|
|to_utf8(String x)|String|返回UTF-8编码格式的字符串|>select to_utf8('info')<br />aW5mbw==|
|locate(String substr, String str)|Int|返回字符串 str 中 substr 的首个出现位置，如果没有则返回 0|>select locate(".", "3.14")<br />2|
|position(String substr, String str)|Int|locate() 的别名|select position(".", "3.14")<br />2|
|concat(String A, String B...)|String|返回所有参数按照传入顺序拼接成的字符串|>select concat("foo", "bar")<br />foobar|
|regexp_like(String str, String regexp)|Boolean|字符串是否匹配给定的正则表达式|>select regexp_like("abc", "[a-z]+")<br />true|
|regexp_extract(String str, String regexp)|String|从字符串中提取出第一个符合正则表达式的子串|>select regexp_extract("abc", "[a-z]+")<br />abc|
|regexp_extract_all(String str, String regexp)|Array<String\>|从字符串中提取出所有符合正则表达式的子串|>select regexp_extract_all("abc22abc", "[a-z]+")<br />[abc,abc]|

### 数学函数

|函数签名|返回值|描述|示例|
|:--|:--|:--|:--|
|abs(Double a), abs(Int a)|Double/Int|计算绝对值|>select abs(-2)<br />2|
|sqrt(Double a)|Double|计算平方根|>select sqrt(100)<br />10|
|greatest(T v1, T v2, ...)|T|计算参数中的最大值，如果任何一个参数是 Null，则返回 Null|>select greatest(1, 3.14, -5)<br />3.14|
|least(T v1, T v2, ...)|T|计算参数中的最小值，如果任何一个参数是 Null，则返回 Null|>select least(1, 3.14, -5)<br />-5|
|rand()|Double|返回一个0到1之间的随机数，数据集的每一行得到的随机数不同|>select rand()<br />0.3|
|ceil(Double a)|Int|对 a 进行向上取整数|>select ceil(3.14)<br />4|
|floor(Double a)|Int|对 a 进行向下取整数|>select floor(3.14)<br />3|
|log(Double a)|Double|计算 a 以2为底的对数值|>select log(32)<br />5|
|ln(Double a)|Double|计算 a 的自然对数|>select  ln(100)<br />4.61512051684126|
|pow(Double a， Double p)|Double|计算 a 的 p 次方|>select pow(2, 5)<br />32|
|round(Key， n)|Double|对 Key 进行四舍五入且保留n位小数|>select round(200.3333, 2)<br />200.33|

### 估算函数
|函数签名|返回值|描述|示例|
|:--|:--|:--|:--|
|percentile(Double x, Double percentage01, Double percentage02...)|Array<Double\>|对x进行正序排列，返回处于percentage01、percentage02...位置的x|>select percentile(latency, 0.1, 0.2)<br/>[0.22, 0.35]|
| approx_set(col)| Hyperloglog| 使用hll算法估算不重复的行数，与cardinality函数一起使用 | >select cardinality(approx_set(num)) <br /> 20 |
 approx_percentile(col,percentage )| Float | 使用t-digest算法估算的百分位数 | >select approx_percentile(num, 0.5) <br /> 10.25|
|approx_percentile(col,array[percentage...] )| Array<Float\> | 使用t-digest算法估算的百分位数，多个百分位数组 | >select approx_percentile(num, array[0.5,0.25]) <br /> [10.25,7.13]|
|approx_percentile(col,weight,percentage )| Float | 使用t-digest算法估算的带权百分位数 | >select approx_percentile(num,weight, 0.5) <br /> 8.45|
|approx_percentile(col,weight,array[percentage...] )| Array<Float\> | 使用t-digest算法估算的带权百分位，多个百分位数组 | >select approx_percentile(num,weight, array[0.3,0.4]) <br /> [8.2,5.6]|

### 日期时间函数
#### 基本函数

|函数签名|返回值|描述|示例|
|:--|:--|:--|:--|
| now()                                                        | DateTime  | 返回当前日期和时间                                             | >select now()<br />2020-01-16T08:30:50Z                      |
| current_timestamp()                                          | DateTime  | now() 的别名                                                 |                                                              |
| unix_timestamp(\[String/DateTime date\[, String format\]\])  | Int       | 将日期时间字符串或 DateTime 类型数值按照 format 格式转换成 Unix timestamp。默认支持 ISO8601 格式，根据字符串中的时区解析。如果根据 format 格式解析，将使用本地时区。 | >select unix_timestamp("2019-11-11T11:11:11Z")<br />1573470671<br />>select unix_timestamp("2019-11-11 11:11:11", "%Y-%m-%d %H:%i:%s")<br />1573441871 |
| from_unixtime(Int unixtime\[, String format\])               | String    | 将 unixtime（从 1970-01-01 00:00:00 UTC 到现在到秒数）转换成表示本地时间的字符串，默认格式为"1970-01-01 00:00:00"，可以通过 format 指定字符串格式。支持的 date_format 请参考[附录](#附录) | >select from_unixtime(0)<br />1970-01-01 08:00:00<br />>select from_unixtime(unix_timestamp("2019-11-11T11:11:11+08:00"))<br />2019-11-11 11:11:11 |
| str_to_date(String str, String format)                       | DateTime  | 根据 format 解析日期时间字符串 str                           | >select str_to_date("2019-11-11 11:11:11", "%Y-%m-%d %H:%i:%s")<br />2019-11-11T03:11:11Z |
| year(String/DateTime date)                                   | Int       | 返回日期 date 的年份                                         | >select year("2019-11-07T09:09:16+08:00")<br />2019          |
| quarter(String/DateTime date)                                | Int       | 返回日期 date 的季度                                         | >select quarter("2019-11-07T09:09:16+08:00")<br />4          |
| month(String/DateTime date)                                  | Int       | 返回日期 date 的月份                                         | >select month("2019-11-07T09:09:16+08:00")<br />11           |
| day(String/DateTime date)                                    | Int       | dayofmonth() 的别名                                          |                                                              |
| hour(String/DateTime date)                                   | Int       | 返回日期 date 的小时                                         | >select hour("2019-11-07T09:09:16+08:00")<br />9             |
| minute(String/DateTime date)                                 | Int       | 返回日期 date 的分钟                                         | >select minute("2019-11-07T09:09:16+08:00")<br />9             |
| second(String/DateTime date)                                 | Int       | 返回日期 date 的秒数                                         | >select second("2019-11-07T09:09:16+08:00")<br />16            |
| weekday(String/DateTime date)                                | Int       | 返回日期 date 在一星期中的位置 (0 = 星期一, 1 = 星期二, ... 6 = 星期日) | >select weekday("2019-11-07T09:09:16+08:00")<br />3          |
| dayofyear(String/DateTime date)                              | Int       | 返回日期 date 在一年中的位置，可选值从 1 到 366              | >select  dayofyear("2019-11-07T09:09:16+08:00")<br />311     |
| dayofmonth(String/DateTime date)                             | Int       | 返回日期 date 在一个月中的位置                               | >select  dayofmonth("2019-11-07T09:09:16+08:00")<br />7      |
| dayofweek(String/DateTime date)                              | Int       | 返回日期 date 在一星期中的位置 (1 = 星期日, 2 = 星期一, ... 7 = 星期六) | >select dayofweek("2019-11-07T09:09:16+08:00")<br />5        |
| current_timezone()                                           | String    | 返回当前时区                                                 | >select current_timezone()<br />Asia/Shanghai                |
| current_date                                                 | String    | 返回当前日期                                                 | >select current_date()<br />2019-11-07                   |
| extract(String unit, String/DateTime date)                   | String    | 根据时间单位提取出当前日期的特定值<br />unit可选为"second/minute/hour/day/month/year" | >select extract("day", "2019-11-07T09:09:16+08:00")<br />7   |
| date_trunc(String unit, String/DateTime date)                | DateTime  | 根据时间单位将日期截断<br />unit可选为"second/minute/hour/day/month/year" | >select date_trunc("day", "2019-11-07T09:09:16+08:00")<br />2019-11-07T00:00:00 |
| date_diff(String unit, String/DateTime start, String/DateTime end) | Int       | 根据时间单位，计算两个时间段之间的差值。小时/分钟/秒/日是精确值，年和月份是提取后的差值<br />unit可选为"second/minute/hour/day/month/year" | >select date_diff("day","2019-11-05T09:09:16+08:00","2019-11-07T09:09:16+08:00")<br />2 |
| date_add(String unit, Int N, DateTime time)           | TimeStamp | 获取time后N个时间单位unit得到的时间<br />unit可选为"second/minute/hour/day/month/year" | >select date_add('day', 2 ,cast('2025-08-15T19:28:42Z+08:00' as timestamp)) <br />2025-08-17 19:28:42.000 |
| localtime()                                                  | String    | 获取当前时间(HH:MM:SS)                                       | >select localtime()<br />10:09:33                            |
| date(String/DateTime time)                                   | String    | 获取对应日期(yy-mm-dd)                                       | >select date("2019-11-05T09:09:16+08:00")<br />2019-11-05    |
| from_iso8601_timestamp(String time)                          | String    | 将ISO8601格式的日期和时间表达式转化为timestamp类型且包含时区的表达式 | >select from_iso8601_timestamp("2019-11-05T09:09:16+08:00")<br />2019-11-05 09:09:16 Asia/Shanghai |
| from_iso8601_date(String time)                               | String    | 将ISO8601格式的日期表达式转化为只包含年月日的字符串          | >select from_iso8601_date("2019-11-05T09:09:16+08:00")<br />2019-11-05 |

#### 时间分组函数

函数描述：持按固定时间间隔对日志数据进行分组聚合统计，例如统计每5分钟的访问次数等场景

函数格式：histogram(time_column, interval)

参数说明：

| 参数| 说明 |
| --- | --- |
| time_column | 时间列（KEY），例如 @timestamp,该列的值必须为毫秒的 long 类型 unix 时间戳或 timestamp 类型的日期时间表达式。如果时间列不符合上述要求，可以使用 cast 函数将 ISO8601 格式的时间字符串转换为 timestamp 类型，例如cast('2020-08-19T03:18:29.000Z' as timestamp)<br />注意：时间列使用 timestamp 时，其对应的日期时间表达式需要为 UTC+0 时区。如果日期时间表达式本身为其他时区，需通过计算调整为 UTC+0 时区。例如原始时间为北京时间（UTC+8）时，使用cast('2020-08-19T03:18:29.000Z' as timestamp) - interval 8 hour进行调整。 |
|interval| 固定时间间隔，支持单位为 second（秒）、minute（分）、hour（小时）、day（天）、week(周)、month(月)。例如时间间隔5分钟，即 interval 5 minute。| 

示例：

统计每5分钟访问次数 PV 值：select histogram(cast(@timestamp as timestamp),interval 5 minute) as t,count(*) group by t order by t



### 条件函数

|函数签名|返回值|描述|示例|
|:--|:--|:--|:--|
|if(Boolean Condition, T valueTrue, T valueFalseOrNull)|T|如果测试条件为 true，返回 ValueTrue，否则返回 ValueFalseOrNull|>select if(2>1, 1, 0)<br />1|
|nullif(T a, T b)|T|如果 a = b，返回 Null，否则返回 a|>select nullif(1, 1)<br />null|
|coalesce(T v1, T v2, ...)|T|返回第一个不是 Null 的值，如果参数都是 Null，返回 Null|>select coalesce(null, 0, false, 1)<br />0|
|CASE a WHEN b THEN c \[WHEN d THEN e\]* \[ELSE f\] END|T|如果 a = b，返回 c；如果 a = d，返回 e；否则返回 f|>select case substring("abc", 1, 1) when "a" then "a" when "b" then "b" else "c" end<br />a|
|CASE WHEN a THEN b \[WHEN c THEN d\]* \[ELSE e\] END|T|如果 a = true，返回 b；如果 c = true，返回 d；否则返回 e|>select case when substring("abc", 1, 1) = "a" then "a" when 2 > 1 then "b" else "c" end<br />a|
### 同比环比函数

| 函数签名| 返回值| 描述 | 示例|
|:--|:--|:--|:--|
|compare(x, t1, t2...)| array<float\> | 对比当前时间窗口内的计算结果与t1, t2.....秒之前时间窗口的计算结果。<br />返回值格式为[当前计算结果, t秒前的计算结果, 当前计算结果与T秒前计算结果的比值]。 | >select compare(x, 3600) from (<br />select avg(latency) as x<br />)<br />[0.3,0.6,0.5] |
| ts_compare(x,t1, t2...) | array<float\> | 在应用时间戳的情况下，对比当前时间窗口内的计算结果与t1, t2.....秒之前时间窗口的计算结果。<br />返回值格式为[当前计算结果, t秒前的计算结果, 当前计算结果与T秒前计算结果的比值]。<br />对应时间窗口t1（如3600）的的计算结果的分组时间戳（如2019-11-01 10:00），会自动补齐时间至（2019-11-01 11:00）与当前的时间戳在一起计算比值 | >select time, ts_compare(x, 3600) from (<br />select time, avg(latency) as x group by time<br />)<br />2019-11-01 12:00,[0.4,0.2,2]<br />2019-11-01 11:00, [0.3,0.6,0.5] |

### Map映射函数

| 函数名称 | 语法 | 说明 | 样例 |
| :--- | :--- | :--- | :--- |
| histogram 函数 | histogram(KEY) | 对检索分析结果进行分组统计数量，返回结果为 JSON 格式。 |>select histogram(level) <br>{"level":30, "warn":20}</br>|
| 下标运算符 | [x] | 返回 Map 中目标键的值。 | > select histogram(level)['info'] <br>20</br>|
| cardinality 函数 | cardinality(KEY) | 计算 Map 中键值对的数量。 | >select cardinality(histogram(level)) <br>2</br> |
| map_keys 函数 | map_keys(KEY) | 提取 Map 中所有的键，并以数组形式返回。 |>select map_keys(histogram(level)) <br>[level,info]</br> |
| map_values 函数 | map_values(KEY) | 提取 Map 中所有键的对应值，并以数组形式返回。 |>select map_values(histogram(level)) <br>[20,10]</br> | 
| map_agg 函数 | map_agg(KEY1, KEY2) | 聚合数据并将其映射为一个 Map。每个键对应一个唯一的值。 |>select map_agg(level, status) <br>{"info":200, "error":500}</br> |
| map 函数 | map() | 构造一个空 map |>select map() <br>{}</br> |
| map 函数 | map(KEY1, KEY2) | 用两个数组构造成一个 map |>select map(array[1,2], array[1,2]) <br>{1:1,2:2}</br> | 
| map_filter 函数 | map_filter(KEY, lambda) | 结合 Lambda 表达式，用于过滤 Map 中的元素 |>select map_filter(map(array[1,2], array[1,2]),(x,y)->x>1) <br>{2:2}</br> ||

### Array数组函数

| 函数签名| 返回值| 描述 | 示例|
|:--|:--|:--|:--|
|group_array(T x)| Array类型 | group_array函数会以数组形式返回x中的所有值 | >select group_array(level) </br> [1,2]|
|array_distinct(Array x)| Array类型| array_distinct函数用于删除数组中重复的元素 | >select array_distinct(array[1,2,2]) </br> [1,2] |

### JSON函数

| 函数签名| 返回值| 描述 | 示例|
|:--|:--|:--|:--|
|json_extract(String json, String path)| String| 从JSON字符串中提取指定path的内容 | >select json_extract('{"a": "a1", "b": "b1"}', '$.a') <br /> a1 |
|json_extract_scalar(String json, String path)| String| JSON对象或JSON数组中提取一组标量值（字符串、整数或布尔值| >select json_extract_scalar('{"a": "a1", "b": "b1"}', '$.a') <br /> a1|
|json_parse(String json)|  String | 用于将字符串类型转化成JSON类型，判断是否符合JSON格式。一般情况下，json_parse函数使用意义不大，如果您需要从JSON中提取值，建议使用json_extract_scalar函数 | >select json_parse('["a", "b"]') <br /> ["a", "b"]|
|json_format(String json)| String| 将JSON类型转化成字符串类型 | >select json_format('["a", "b"]') <br /> ["a", "b"]|
|json_size(String json, String path)|Int | 计算JSON对象或数组中元素的数量 | >select json_size('{"a": "a1", "b": "b1"}') <br /> 2 |
|json_array_contains(String json, T item)| Boolean | 判断JSON数组中是否包含某个值 | >select json_array_contains('["a", "b"]', 'a') <br /> true |
|json_array_get(String json, Int index)| String | 获取JSON数组中某个下标对应的元素 | >select json_array_get('["a", "b"]', 0) <br /> a |
|json_array_length(String json)| Int | 计算JSON数组中元素的数量 | >select json_array_length('["a", "b"]') <br /> 2 |


## IP函数
| 函数签名| 返回值| 描述 | 示例|
|:--|:--|:--|:--|
|ip_prefix(x, prefix_bits)| String | 获取目标IPv4地址的前缀 | >select ip_prefix('192.168.1.1', 20) <br /> 192.168.0.0/20 |
|is_prefix_subnet_of(x, y)| Bool | 判断目标IPv4网段是否为某网段的子网 | >select is_prefix_subnet_of('192.168.0.1/24','192.169.1.1/24') <br /> false |
|is_subnet_of(x, y)| Bool | 判断目标IPv4地址是否在某网段内 | >select  is_subnet_of('192.168.0.1/24','192.168.0.24') <br /> true |
|ip_subnet_max(x)| String | 获取IPv4网段中的最大IP地址 | >select ip_subnet_max('127.0.0.1/24') <br /> 127.0.0.255 |
|ip_subnet_min(x)| String | 获取IPv4网段中的最小IP地址 | >select ip_subnet_min('127.0.0.1/24') <br />	127.0.0.0 |
|ip_subnet_range(x)| Array(String) | 获取IPv4网段范围 | >select ip_subnet_range('127.0.0.1/24') <br /> [127.0.0.0,127.0.0.255] |
|ip_to_city(x)| String | 获取目标IPv4地址的城市 | >select ip_to_city('114.114.114.114') <br /> 南京 |

## 附录

### 日期格式

时间函数支持的 date_format

|占位符|描述|
|:--|:--|
|%a|Abbreviated weekday name (Sun..Sat)|
|%b|Abbreviated month name (Jan..Dec)|
|%c|Month, numeric (0..12)|
|%D|Day of the month with English suffix (0th, 1st, 2nd, 3rd, …)|
|%d|Day of the month, numeric (00..31)|
|%e|Day of the month, numeric (0..31)|
|%f|Microseconds (000000..999999)|
|%H|Hour (00..23)|
|%h|Hour (01..12)|
|%I|Hour (01..12)|
|%i|Minutes, numeric (00..59)|
|%j|Day of year (001..366)|
|%k|Hour (0..23)|
|%l|Hour (1..12)|
|%M|Month name (January..December)|
|%m|Month, numeric (00..12)|
|%p|AM or PM|
|%r|Time, 12-hour (hh:mm:ss followed by AM or PM)|
|%S|Seconds (00..59)|
|%s|Seconds (00..59)|
|%T|Time, 24-hour (hh:mm:ss)|
|%W|Weekday name (Sunday..Saturday)|
|%w|Day of the week (0=Sunday..6=Saturday)|
|%Y|Year, numeric, four digits|
|%y|Year, numeric (two digits)|
|%%|A literal % character|