[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [base](../modules/base.md) / BMStringUtils

# Class: BMStringUtils

[base](../modules/base.md).BMStringUtils

string 相关的工具类

## Table of contents

### Constructors

- [constructor](base.BMStringUtils.md#constructor)

### Methods

- [isNull](base.BMStringUtils.md#isnull)
- [isNotNull](base.BMStringUtils.md#isnotnull)
- [isEmpty](base.BMStringUtils.md#isempty)
- [isNotEmpty](base.BMStringUtils.md#isnotempty)
- [replace](base.BMStringUtils.md#replace)
- [replaceAll](base.BMStringUtils.md#replaceall)
- [stripHtmlTags](base.BMStringUtils.md#striphtmltags)
- [startsWith](base.BMStringUtils.md#startswith)
- [endsWith](base.BMStringUtils.md#endswith)
- [contains](base.BMStringUtils.md#contains)
- [equal](base.BMStringUtils.md#equal)
- [equalsIgnoreCase](base.BMStringUtils.md#equalsignorecase)
- [split](base.BMStringUtils.md#split)
- [toLower](base.BMStringUtils.md#tolower)
- [toUpper](base.BMStringUtils.md#toupper)
- [capitalize](base.BMStringUtils.md#capitalize)
- [strToUint8Array](base.BMStringUtils.md#strtouint8array)
- [unit8ArrayToStr](base.BMStringUtils.md#unit8arraytostr)
- [strToHex](base.BMStringUtils.md#strtohex)
- [hexToStr](base.BMStringUtils.md#hextostr)
- [strToBase64](base.BMStringUtils.md#strtobase64)
- [base64ToStr](base.BMStringUtils.md#base64tostr)
- [strToBuffer](base.BMStringUtils.md#strtobuffer)
- [bufferToStr](base.BMStringUtils.md#buffertostr)
- [bufferToUint8Array](base.BMStringUtils.md#buffertouint8array)
- [unit8ArrayToBuffer](base.BMStringUtils.md#unit8arraytobuffer)
- [trimParentheses](base.BMStringUtils.md#trimparentheses)
- [copyArray](base.BMStringUtils.md#copyarray)
- [format](base.BMStringUtils.md#format)
- [toDouble](base.BMStringUtils.md#todouble)

## Constructors

### constructor

• **new BMStringUtils**(): [`BMStringUtils`](base.BMStringUtils.md)

#### Returns

[`BMStringUtils`](base.BMStringUtils.md)

## Methods

### isNull

▸ **isNull**(`str`): `boolean`

字符串是否为空(undefined、null)

#### Parameters

| Name | Type |
| :------ | :------ |
| `str` | `undefined` \| ``null`` \| `string` |

#### Returns

`boolean`

___

### isNotNull

▸ **isNotNull**(`str`): `boolean`

判断字符串是否为非空。true为非空，否则false

#### Parameters

| Name | Type |
| :------ | :------ |
| `str` | `undefined` \| ``null`` \| `string` |

#### Returns

`boolean`

___

### isEmpty

▸ **isEmpty**(`str`): `boolean`

字符串是否为空(undefined、null、字符串长度为0)

#### Parameters

| Name | Type |
| :------ | :------ |
| `str` | `undefined` \| ``null`` \| `string` |

#### Returns

`boolean`

___

### isNotEmpty

▸ **isNotEmpty**(`str`): `boolean`

判断字符串是否为非空。true为非空空，否则false

#### Parameters

| Name | Type |
| :------ | :------ |
| `str` | `undefined` \| ``null`` \| `string` |

#### Returns

`boolean`

___

### replace

▸ **replace**(`str`, `pattern`, `replacement?`): `string`

替换字符串中匹配的正则为给定的字符串

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `str` | `string` | `undefined` | 待替换的字符串 |
| `pattern` | `string` \| `RegExp` | `undefined` | 要匹配的内容正则或字符串 |
| `replacement` | `string` | `''` | 替换的内容 |

#### Returns

`string`

返回替换后的字符串

___

### replaceAll

▸ **replaceAll**(`str`, `pattern`, `replacement?`): `string`

替换字符串中所有匹配的正则为给定的字符串

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `str` | `string` | `undefined` | 待替换的字符串 |
| `pattern` | `string` \| `RegExp` | `undefined` | 要匹配的内容正则或字符串 |
| `replacement` | `string` | `''` | 替换的内容 |

#### Returns

`string`

返回替换后的字符串

___

### stripHtmlTags

▸ **stripHtmlTags**(`str`): `string`

去除字符串中的 HTML 标签

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `str` | `string` | 待处理的字符串 |

#### Returns

`string`

去除标签后的字符串

___

### startsWith

▸ **startsWith**(`string?`, `target`, `position?`): `boolean`

检查字符串是否以给定的字符串开头

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `string` | `string` | `''` | 源字符串 |
| `target` | `string` | `undefined` | 要检索字符 |
| `position` | `number` | `0` | 检索的位置 |

#### Returns

`boolean`

如果字符串以字符串开头，那么返回 true，否则返回 false

___

### endsWith

▸ **endsWith**(`str?`, `target`, `position?`): `boolean`

检查字符串是否以给定的字符串结尾

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `str` | `string` | `''` | 源字符串 |
| `target` | `string` | `undefined` | 要检索字符 |
| `position` | `number` | `str.length` | 检索的位置 |

#### Returns

`boolean`

如果字符串以字符串结尾，那么返回 true，否则返回 false

___

### contains

▸ **contains**(`str?`, `target`): `boolean`

检查字符串是否包含给定的字符串

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `str` | `string` | `''` | 源字符串 |
| `target` | `string` | `undefined` | 要检索字符 |

#### Returns

`boolean`

如果str包含target，返回true，否则返回false

___

### equal

▸ **equal**(`source`, `target`): `boolean`

判断两个传入的数值或者是字符串是否相等

#### Parameters

| Name | Type |
| :------ | :------ |
| `source` | `string` \| `number` |
| `target` | `string` \| `number` |

#### Returns

`boolean`

___

### equalsIgnoreCase

▸ **equalsIgnoreCase**(`source`, `target`): `boolean`

判断两个传入的数值或者是字符串是否相等

#### Parameters

| Name | Type |
| :------ | :------ |
| `source` | `string` \| `number` |
| `target` | `string` \| `number` |

#### Returns

`boolean`

___

### split

▸ **split**(`str`, `separator`): `string`[]

字符串分割

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `str` | `undefined` \| ``null`` \| `string` | 源字符串 |
| `separator` | `string` \| `RegExp` | 分割符 |

#### Returns

`string`[]

分割后的字符串数组

___

### toLower

▸ **toLower**(`str?`): `string`

转换整个字符串的字符为小写

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `str` | `string` | `''` | 要转换的字符串 |

#### Returns

`string`

返回小写的字符串

___

### toUpper

▸ **toUpper**(`str?`): `string`

转换整个字符串的字符为大写

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `str` | `string` | `''` | 要转换的字符串 |

#### Returns

`string`

返回小写的字符串

___

### capitalize

▸ **capitalize**(`str?`): `string`

转换字符串首字母为大写，剩下为小写

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `str` | `string` | `''` | 待转换的字符串 |

#### Returns

`string`

转换后的

___

### strToUint8Array

▸ **strToUint8Array**(`src`, `encoding?`): `Uint8Array`

字符串转Uint8Array

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `src` | `string` | `undefined` | 字符串 |
| `encoding` | `BufferEncoding` | `'utf-8'` | - |

#### Returns

`Uint8Array`

Uint8Array

___

### unit8ArrayToStr

▸ **unit8ArrayToStr**(`src`, `encoding?`): `string`

Uint8Array转字符串

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `src` | `Uint8Array` | `undefined` | Uint8Array |
| `encoding` | `BufferEncoding` | `'utf-8'` | - |

#### Returns

`string`

字符串

___

### strToHex

▸ **strToHex**(`hexStr`): `Uint8Array`

16进制字符串转换unit8Array

#### Parameters

| Name | Type |
| :------ | :------ |
| `hexStr` | `string` |

#### Returns

`Uint8Array`

___

### hexToStr

▸ **hexToStr**(`arr`): `string`

16进制unit8Array转字符串

#### Parameters

| Name | Type |
| :------ | :------ |
| `arr` | `Uint8Array` |

#### Returns

`string`

___

### strToBase64

▸ **strToBase64**(`src`): `string`

字符串转Base64字符串

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `src` | `string` | 字符串 |

#### Returns

`string`

___

### base64ToStr

▸ **base64ToStr**(`base64Str`): `string`

Base64字符串转字符串

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `base64Str` | `string` | Base64字符串 |

#### Returns

`string`

___

### strToBuffer

▸ **strToBuffer**(`src`, `encoding?`): `ArrayBuffer`

字符串转ArrayBuffer

#### Parameters

| Name | Type | Default value |
| :------ | :------ | :------ |
| `src` | `string` | `undefined` |
| `encoding` | `BufferEncoding` | `'utf-8'` |

#### Returns

`ArrayBuffer`

___

### bufferToStr

▸ **bufferToStr**(`src`, `encoding?`): `string`

ArrayBuffer转字符串

#### Parameters

| Name | Type | Default value |
| :------ | :------ | :------ |
| `src` | `ArrayBuffer` | `undefined` |
| `encoding` | `BufferEncoding` | `'utf-8'` |

#### Returns

`string`

___

### bufferToUint8Array

▸ **bufferToUint8Array**(`src`): `Uint8Array`

ArrayBuffer转Uint8Array

#### Parameters

| Name | Type |
| :------ | :------ |
| `src` | `ArrayBuffer` |

#### Returns

`Uint8Array`

___

### unit8ArrayToBuffer

▸ **unit8ArrayToBuffer**(`src`): `ArrayBuffer`

Uint8Array转ArrayBuffer

#### Parameters

| Name | Type |
| :------ | :------ |
| `src` | `Uint8Array` |

#### Returns

`ArrayBuffer`

___

### trimParentheses

▸ **trimParentheses**(`str?`): `string`

去除字符串首尾的小括号

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `str` | `string` | `""` | 待处理的字符串，默认为空字符串 |

#### Returns

`string`

去除首尾小括号后的字符串

___

### copyArray

▸ **copyArray**(`target`): `string`[]

复制数组

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `target` | `undefined` \| ``null`` \| `string`[] | 目标数组 |

#### Returns

`string`[]

复制后的数组

___

### format

▸ **format**(`formatString`, `...values`): `string`

字符串format方法

#### Parameters

| Name | Type |
| :------ | :------ |
| `formatString` | `string` |
| `...values` | (`undefined` \| ``null`` \| `string` \| `number` \| `boolean`)[] |

#### Returns

`string`

___

### toDouble

▸ **toDouble**(`str`): ``null`` \| `number`

#### Parameters

| Name | Type |
| :------ | :------ |
| `str` | `string` |

#### Returns

``null`` \| `number`
