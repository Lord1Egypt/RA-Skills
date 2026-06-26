# Smali 语法快速参考

## 基本结构

```smali
.class public Lcom/example/MyClass;
.super Landroid/app/Activity;
.source "MyClass.java"
```

## 字段定义

```smali
# 静态字段
.field private static final TAG:Ljava/lang/String; = "MyClass"

# 实例字段
.field private mName:Ljava/lang/String;
.field private mCount:I
```

## 方法定义

```smali
.method public constructor <init>()V
    .registers 1
    invoke-direct {p0}, Landroid/app/Activity;-><init>()V
    return-void
.end method

.method public getName()Ljava/lang/String;
    .registers 2
    iget-object v0, p0, Lcom/example/MyClass;->mName:Ljava/lang/String;
    return-object v0
.end method
```

## 寄存器

- `p0` = this (非静态方法)
- `p1`, `p2`, ... = 参数
- `v0`, `v1`, ... = 局部变量

## 常用指令

### 数据移动
```smali
move v0, v1          # v0 = v1
move-wide v0, v2     # 64位移动
move-object v0, v1   # 对象引用
const/4 v0, 0x1      # v0 = 1
const-string v0, "Hello"
```

### 字段访问
```smali
iget v0, p0, Lcom/example/MyClass;->mCount:I    # 读取实例字段
iput v0, p0, Lcom/example/MyClass;->mCount:I    # 写入实例字段
sget v0, Lcom/example/MyClass;->TAG:Ljava/lang/String;  # 读取静态字段
sput v0, Lcom/example/MyClass;->TAG:Ljava/lang/String;  # 写入静态字段
```

### 方法调用
```smali
invoke-virtual {p0, p1}, Lcom/example/MyClass;->doSomething(I)V
invoke-static {}, Lcom/example/Helper;->getInstance()Lcom/example/Helper;
invoke-direct {p0}, Landroid/app/Activity;-><init>()V
invoke-interface {v0}, Ljava/util/List;->size()I
```

### 条件跳转
```smali
if-eq v0, v1, :cond_0    # if (v0 == v1) goto cond_0
if-ne v0, v1, :cond_0    # if (v0 != v1) goto cond_0
if-lt v0, v1, :cond_0    # if (v0 < v1) goto cond_0
if-ge v0, v1, :cond_0    # if (v0 >= v1) goto cond_0
if-eqz v0, :cond_0       # if (v0 == 0) goto cond_0
if-nez v0, :cond_0       # if (v0 != 0) goto cond_0
```

### 数组操作
```smali
new-array v0, v1, [I          # int[] v0 = new int[v1]
aget v0, v1, v2               # v0 = v1[v2]
aput v0, v1, v2               # v1[v2] = v0
array-length v0, v1           # v0 = v1.length
```

### 类型检查
```smali
instance-of v0, v1, Ljava/lang/String;   # v0 = (v1 instanceof String)
check-cast v0, Ljava/lang/String;        # v0 = (String) v0
new-instance v0, Ljava/lang/String;      # v0 = new String()
```

## 类型描述符

| Java 类型 | Smali 描述符 |
|-----------|--------------|
| void      | V            |
| boolean   | Z            |
| byte      | B            |
| char      | C            |
| short     | S            |
| int       | I            |
| long      | J            |
| float     | F            |
| double    | D            |
| String    | Ljava/lang/String; |
| int[]     | [I           |
| String[]  | [Ljava/lang/String; |

## 修改示例

### 修改字符串常量
```smali
# 原来
const-string v0, "Hello"

# 修改后
const-string v0, "World"
```

### 修改条件判断
```smali
# 原来
if-nez v0, :cond_0

# 修改后（总是跳转）
goto :cond_0
```

### 添加日志
```smali
const-string v0, "TAG"
const-string v1, "Debug message"
invoke-static {v0, v1}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I
```

### 禁用广告/检查
```smali
# 找到检查方法，直接返回
.method public shouldShowAd()Z
    .registers 1
    const/4 v0, 0x0
    return v0
.end method
```

## 重新打包流程

1. 修改 `.smali` 文件
2. 运行 `python3 rebuild.py ./project-dir`
3. 安装测试：`adb install app-rebuilt.apk`
