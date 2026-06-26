---
outline: deep
---
 # Point


## Point

**`该类表示一个二维点坐标`**

### Examples

```javascript
const point = new DiMap.Point(100, 200)
```

### x

**`x 坐标`**

Type: <span>[number][1]</span>

### y

**`y 坐标`**

Type: <span>[number][1]</span>

### convert

**`将给定的对象转换为Point对象。`**

#### Parameters

*   `a` **[PointLike][2]** 点坐标

Returns **[Point][3]**&#x20;

### constructor

**`创建一个点对象`**

#### Parameters

*   `x` **[number][1]** x 轴坐标值
*   `y` **[number][1]** y 轴坐标值

### clone

**`复制一个点对象，返回一个新点对象，对新点对象的修改不会影响原来的点对象`**

Returns **[Point][3]** 返回一个新的 Point 对象

### add

**`当前点对象的x,y值与另一个点对象的x,y值相加，返回一个新点对象`**

#### Parameters

*   `p` **[Point][3]** 另一个点对象

Returns **[Point][3]** 返回一个新的 Point 对象

### sub

**`当前点对象的x,y值与另一个点对象的x,y值相减，返回一个新点对象`**

#### Parameters

*   `p` **[Point][3]** 另一个点对象

Returns **[Point][3]** 返回一个新的 Point 对象

### mult

**`缩放当前点对象,x,y各自乘以k, 返回一个新点对象`**

#### Parameters

*   `k` **[number][1]** 缩放比例

Returns **[Point][3]** 返回一个新的 Point 对象

### div

**`缩放当前点对象,x,y各自除以k, 返回一个新点对象`**

#### Parameters

*   `k` **[number][1]** 缩放比例

Returns **[Point][3]** 返回一个新的 Point 对象

### rotate

**`旋转当前点对象`**

#### Parameters

*   `a` **[number][1]** 旋转角度，单位为弧度

Returns **[Point][3]** 返回一个新的 Point 对象，表示当前点对象旋转后的结果

### matMult

**`与一个 2x2 矩阵相乘，得到一个新的点对象`**

#### Parameters

*   `m` **[Array][4]<[number][1]>** 一个长度为 4 的数组，表示一个 2x2 的矩阵，其中 m\[0] 和 m\[1] 表示第一行的两个元素，m\[2] 和 m\[3] 表示第二行的两个元素

Returns **[Point][3]** 返回一个新的 Point 对象，表示当前点对象与矩阵相乘的结果

### unit

**`返回当前点对象的单位向量`**

Returns **[Point][3]** 返回一个新的 Point 对象，表示当前点对象的单位向量

### perp

**`返回当前点对象的垂直向量`**

Returns **[Point][3]** 返回一个新的 Point 对象，表示当前点对象的垂直向量

### round

**`返回当前点对象的四舍五入整数点坐标`**

Returns **[Point][3]** 返回一个新的 Point 对象，表示当前点对象四舍五入后的结果

### round

**`将当前点的x和y坐标四舍五入到最接近的整数，并返回结果的新点。`**

Returns **[Point][3]** 四舍五入的新点

### mag

**`返回当前点与原点之间的距离。`**

Returns **[number][1]** 当前点与原点之间的距离

### equals

**`如果给定的点与当前点相同，则返回true，否则返回false。`**

#### Parameters

*   `p` **[Point][3]** 要比较的点

Returns **[boolean][5]** 如果给定的点与当前点相同，则为true，否则为false

### dist

**`返回当前点到给定点之间的距离。`**

#### Parameters

*   `p` **[Point][3]** 要计算距离的点

Returns **[number][1]** 当前点到给定点之间的距离

### distSqr

**`返回当前点到给定点之间的距离的平方。`**

#### Parameters

*   `p` **[Point][3]** 要计算距离的点

Returns **[number][1]** 当前点到给定点之间的距离的平方

### angle

**`返回从当前点到原点的线段与x轴之间的角度（以弧度为单位）。`**

Returns **[number][1]** 当前点到原点的线段与x轴之间的角度（以弧度为单位）

### angleTo

**`返回从当前点到给定点之间的线段与x轴之间的角度（以弧度为单位）。`**

#### Parameters

*   `p` **[Point][3]** 终点

Returns **[number][1]** 当前点到给定点之间的线段与x轴之间的角度（以弧度为单位）

### angleWidth

**`返回从当前点到给定点之间的线段的宽度（以弧度为单位）。`**

#### Parameters

*   `p` **[Point][3]** 终点

Returns **[number][1]** 当前点到给定点之间的线段的宽度（以弧度为单位）

### angleWithSep

**`返回从当前点到给定坐标之间的线段与x轴之间的角度（以弧度为单位）。`**

#### Parameters

*   `x` **[number][1]** 终点的x坐标
*   `y` **[number][1]** 终点的y坐标

Returns **[number][1]** 当前点到给定坐标之间的线段与x轴之间的角度（以弧度为单位）

[1]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number

[2]: /jsapi/apis/types/Types.html#pointlike

[3]: #point

[4]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array

[5]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Boolean
