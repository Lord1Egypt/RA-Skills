[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [base](../modules/base.md) / BMFileUtils

# Class: BMFileUtils

[base](../modules/base.md).BMFileUtils

文件操作相关工具类

## Table of contents

### Properties

- [separator](base.BMFileUtils.md#separator)

### Methods

- [getFilesDirPath](base.BMFileUtils.md#getfilesdirpath)
- [getCacheDirPath](base.BMFileUtils.md#getcachedirpath)
- [getTempDirPath](base.BMFileUtils.md#gettempdirpath)
- [hasDirPath](base.BMFileUtils.md#hasdirpath)
- [getFileUri](base.BMFileUtils.md#getfileuri)
- [getFileName](base.BMFileUtils.md#getfilename)
- [getFilePath](base.BMFileUtils.md#getfilepath)
- [getParentUri](base.BMFileUtils.md#getparenturi)
- [getParentPath](base.BMFileUtils.md#getparentpath)
- [getUriFromPath](base.BMFileUtils.md#geturifrompath)
- [getFileExtention](base.BMFileUtils.md#getfileextention)
- [getFileDirSize](base.BMFileUtils.md#getfiledirsize)
- [isFile](base.BMFileUtils.md#isfile)
- [isDirectory](base.BMFileUtils.md#isdirectory)
- [rename](base.BMFileUtils.md#rename)
- [renameSync](base.BMFileUtils.md#renamesync)
- [mkdir](base.BMFileUtils.md#mkdir)
- [mkdirSync](base.BMFileUtils.md#mkdirsync)
- [rmdir](base.BMFileUtils.md#rmdir)
- [rmdirSync](base.BMFileUtils.md#rmdirsync)
- [unlink](base.BMFileUtils.md#unlink)
- [unlinkSync](base.BMFileUtils.md#unlinksync)
- [access](base.BMFileUtils.md#access)
- [accessSync](base.BMFileUtils.md#accesssync)
- [open](base.BMFileUtils.md#open)
- [openSync](base.BMFileUtils.md#opensync)
- [read](base.BMFileUtils.md#read)
- [readSync](base.BMFileUtils.md#readsync)
- [readText](base.BMFileUtils.md#readtext)
- [readTextSync](base.BMFileUtils.md#readtextsync)
- [write](base.BMFileUtils.md#write)
- [writeSync](base.BMFileUtils.md#writesync)
- [writeEasy](base.BMFileUtils.md#writeeasy)
- [close](base.BMFileUtils.md#close)
- [closeSync](base.BMFileUtils.md#closesync)
- [listFile](base.BMFileUtils.md#listfile)
- [listFileSync](base.BMFileUtils.md#listfilesync)
- [stat](base.BMFileUtils.md#stat)
- [statSync](base.BMFileUtils.md#statsync)
- [copy](base.BMFileUtils.md#copy)
- [copyFile](base.BMFileUtils.md#copyfile)
- [copyFileSync](base.BMFileUtils.md#copyfilesync)
- [copyDir](base.BMFileUtils.md#copydir)
- [copyDirSync](base.BMFileUtils.md#copydirsync)
- [moveFile](base.BMFileUtils.md#movefile)
- [moveFileSync](base.BMFileUtils.md#movefilesync)
- [moveDir](base.BMFileUtils.md#movedir)
- [moveDirSync](base.BMFileUtils.md#movedirsync)
- [truncate](base.BMFileUtils.md#truncate)
- [truncateSync](base.BMFileUtils.md#truncatesync)
- [lstat](base.BMFileUtils.md#lstat)
- [lstatSync](base.BMFileUtils.md#lstatsync)
- [fsync](base.BMFileUtils.md#fsync)
- [fsyncSync](base.BMFileUtils.md#fsyncsync)
- [fdatasync](base.BMFileUtils.md#fdatasync)
- [fdatasyncSync](base.BMFileUtils.md#fdatasyncsync)
- [createStream](base.BMFileUtils.md#createstream)
- [createStreamSync](base.BMFileUtils.md#createstreamsync)
- [fdopenStream](base.BMFileUtils.md#fdopenstream)
- [fdopenStreamSync](base.BMFileUtils.md#fdopenstreamsync)
- [mkdtemp](base.BMFileUtils.md#mkdtemp)
- [mkdtempSync](base.BMFileUtils.md#mkdtempsync)
- [dup](base.BMFileUtils.md#dup)
- [utimes](base.BMFileUtils.md#utimes)
- [getFormatFileSize](base.BMFileUtils.md#getformatfilesize)
- [getRawFileContentSync](base.BMFileUtils.md#getrawfilecontentsync)
- [getRawFileContent](base.BMFileUtils.md#getrawfilecontent)
- [getRawFileContentStrSync](base.BMFileUtils.md#getrawfilecontentstrsync)
- [getRawFileContentStr](base.BMFileUtils.md#getrawfilecontentstr)
- [saveImage](base.BMFileUtils.md#saveimage)

## Properties

### separator

▪ `Static` `Readonly` **separator**: `string` = `'/'`

## Methods

### getFilesDirPath

▸ **getFilesDirPath**(`dirPath?`, `fileName?`, `blHap?`): `string`

获取文件目录下的文件夹路径或文件路径。

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `dirPath` | `string` | `""` | 文件路径；支持完整路径和相对路径（download/wps/doc）；dirPath传空字符串表示根目录 |
| `fileName` | `string` | `""` | 文件名（test.text）；fileName传空字符串表示文件夹路径 |
| `blHap` | `boolean` | `true` | true：HAP级别文件路径、 false：App级别文件路径 |

#### Returns

`string`

___

### getCacheDirPath

▸ **getCacheDirPath**(`dirPath?`, `fileName?`, `blHap?`): `string`

获取缓存目录下的文件夹路径或文件路径。

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `dirPath` | `string` | `""` | 文件路径；支持完整路径和相对路径（download/wps/doc）；dirPath传空字符串表示根目录 |
| `fileName` | `string` | `""` | 文件名（test.text）；fileName传空字符串表示文件夹路径 |
| `blHap` | `boolean` | `true` | true：HAP级别文件路径、 false：App级别文件路径 |

#### Returns

`string`

___

### getTempDirPath

▸ **getTempDirPath**(`dirPath?`, `fileName?`, `blHap?`): `string`

获取临时目录下的文件夹路径或文件路径。

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `dirPath` | `string` | `""` | 文件路径；支持完整路径和相对路径（download/wps/doc）；dirPath传空字符串表示根目录 |
| `fileName` | `string` | `""` | 文件名（test.text）；fileName传空字符串表示文件夹路径 |
| `blHap` | `boolean` | `true` | true：HAP级别文件路径、 false：App级别文件路径 |

#### Returns

`string`

___

### hasDirPath

▸ **hasDirPath**(`path`): `boolean`

判断是否是完整路径

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `path` | `string` | 文件路径 |

#### Returns

`boolean`

___

### getFileUri

▸ **getFileUri**(`uriOrPath`): `FileUri`

通过URI或路径，获取FileUri

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `uriOrPath` | `string` | URI或路径 |

#### Returns

`FileUri`

___

### getFileName

▸ **getFileName**(`uriOrPath`): `string`

通过URI或路径，获取文件名。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `uriOrPath` | `string` | URI或路径 |

#### Returns

`string`

___

### getFilePath

▸ **getFilePath**(`uriOrPath`): `string`

通过URI或路径，获取文件路径

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `uriOrPath` | `string` | URI或路径 |

#### Returns

`string`

___

### getParentUri

▸ **getParentUri**(`uriOrPath`): `string`

通过URI或路径，获取对应文件父目录的URI。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `uriOrPath` | `string` | URI或路径 |

#### Returns

`string`

___

### getParentPath

▸ **getParentPath**(`uriOrPath`): `string`

通过URI或路径，获取对应文件父目录的路径名。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `uriOrPath` | `string` | URI或路径 |

#### Returns

`string`

___

### getUriFromPath

▸ **getUriFromPath**(`path`): `string`

以同步方法获取文件URI。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `path` | `string` | 应用沙箱路径 |

#### Returns

`string`

___

### getFileExtention

▸ **getFileExtention**(`fileName`): `string`

根据文件名获取文件后缀

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `fileName` | `string` | 例如: test.txt test.doc |

#### Returns

`string`

___

### getFileDirSize

▸ **getFileDirSize**(`path`): `number`

获取指定文件夹下所有文件的大小或指定文件大小。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `path` | `string` | 文件夹路径 或 文件路径 |

#### Returns

`number`

___

### isFile

▸ **isFile**(`file`): `boolean`

判断文件是否是普通文件。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `file` | `string` \| `number` | string\|number 文件应用沙箱路径path或已打开的文件描述符fd。 |

#### Returns

`boolean`

___

### isDirectory

▸ **isDirectory**(`file`): `boolean`

判断文件是否是目录。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `file` | `string` \| `number` | string\|number 文件应用沙箱路径path或已打开的文件描述符fd。 |

#### Returns

`boolean`

___

### rename

▸ **rename**(`oldPath`, `newPath`): `Promise`\<`void`\>

重命名文件或文件夹，使用Promise异步回调。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `oldPath` | `string` | string 文件的应用沙箱原路径。 |
| `newPath` | `string` | string 文件的应用沙箱新路径。 |

#### Returns

`Promise`\<`void`\>

___

### renameSync

▸ **renameSync**(`oldPath`, `newPath`): `void`

重命名文件或文件夹，以同步方法。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `oldPath` | `string` | string 文件的应用沙箱原路径。 |
| `newPath` | `string` | string 文件的应用沙箱新路径。 |

#### Returns

`void`

___

### mkdir

▸ **mkdir**(`path`, `recursion?`): `Promise`\<`void`\>

创建目录，当recursion指定为true，可多层级创建目录，使用Promise异步回调。

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `path` | `string` | `undefined` | 目录的应用沙箱路径。 |
| `recursion` | `boolean` | `true` | 是否多层级创建目录。recursion指定为true时，可多层级创建目录。recursion指定为false时，仅可创建单层目录。 |

#### Returns

`Promise`\<`void`\>

___

### mkdirSync

▸ **mkdirSync**(`path`, `recursion?`): `void`

创建目录以同步方法，当recursion指定为true，可多层级创建目录。

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `path` | `string` | `undefined` | 目录的应用沙箱路径。 |
| `recursion` | `boolean` | `true` | 是否多层级创建目录。recursion指定为true时，可多层级创建目录。recursion指定为false时，仅可创建单层目录。 |

#### Returns

`void`

___

### rmdir

▸ **rmdir**(`path`): `Promise`\<`void`\>

删除整个目录，使用Promise异步回调。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `path` | `string` | 目录的应用沙箱路径。 |

#### Returns

`Promise`\<`void`\>

___

### rmdirSync

▸ **rmdirSync**(`path`): `any`

删除整个目录，以同步方法。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `path` | `string` | 目录的应用沙箱路径。 |

#### Returns

`any`

___

### unlink

▸ **unlink**(`path`): `Promise`\<`void`\>

删除单个文件，使用Promise异步回调。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `path` | `string` | 文件的应用沙箱路径。 |

#### Returns

`Promise`\<`void`\>

___

### unlinkSync

▸ **unlinkSync**(`path`): `void`

删除单个文件，以同步方法。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `path` | `string` | 文件的应用沙箱路径。 |

#### Returns

`void`

___

### access

▸ **access**(`path`): `Promise`\<`boolean`\>

检查文件是否存在，使用Promise异步回调。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `path` | `string` | 文件应用沙箱路径。 |

#### Returns

`Promise`\<`boolean`\>

___

### accessSync

▸ **accessSync**(`path`): `boolean`

检查文件是否存在，以同步方法。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `path` | `string` | 文件应用沙箱路径。 |

#### Returns

`boolean`

___

### open

▸ **open**(`path`, `mode?`): `Promise`\<`File`\>

打开文件，支持使用URI打开文件。使用Promise异步回调。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `path` | `string` | string 文件的应用沙箱路径或URI。 |
| `mode` | `number` | number 打开文件的选项，必须指定如下选项中的一个，默认以只读方式打开。 |

#### Returns

`Promise`\<`File`\>

___

### openSync

▸ **openSync**(`path`, `mode?`): `File`

打开文件，支持使用URI打开文件。以同步方法。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `path` | `string` | string 文件的应用沙箱路径或URI。 |
| `mode` | `number` | number 打开文件的选项，必须指定如下选项中的一个，默认以只读方式打开。 |

#### Returns

`File`

___

### read

▸ **read**(`fd`, `buffer`, `options?`): `Promise`\<`number`\>

从文件读取数据，使用Promise异步回调。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `fd` | `number` | number 已打开的文件描述符。 |
| `buffer` | `ArrayBuffer` | ArrayBuffer 用于保存读取到的文件数据的缓冲区。 |
| `options?` | `any` | 支持如下选项： offset，number类型，表示期望读取文件的位置。可选，默认从当前位置开始读。 length，number类型，表示期望读取数据的长度。可选，默认缓冲区长度。 |

#### Returns

`Promise`\<`number`\>

___

### readSync

▸ **readSync**(`fd`, `buffer`, `options?`): `number`

从文件读取数据，以同步方法。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `fd` | `number` | number 已打开的文件描述符。 |
| `buffer` | `ArrayBuffer` | ArrayBuffer 用于保存读取到的文件数据的缓冲区。 |
| `options?` | `any` | 支持如下选项： offset，number类型，表示期望读取文件的位置。可选，默认从当前位置开始读。 length，number类型，表示期望读取数据的长度。可选，默认缓冲区长度。 |

#### Returns

`number`

___

### readText

▸ **readText**(`filePath`, `options?`): `Promise`\<`string`\>

基于文本方式读取文件（即直接读取文件的文本内容），使用Promise异步回调。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `filePath` | `string` | 文件的应用沙箱路径。 |
| `options?` | `any` | 支持如下选项： offset，number类型，表示期望读取文件的位置。可选，默认从当前位置开始读取。 length，number类型，表示期望读取数据的长度。可选，默认文件长度。 encoding，string类型，当数据是 string 类型时有效，表示数据的编码方式，默认 'utf-8'，仅支持 'utf-8'。 |

#### Returns

`Promise`\<`string`\>

___

### readTextSync

▸ **readTextSync**(`filePath`, `options?`): `string`

基于文本方式读取文件（即直接读取文件的文本内容），以同步方法。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `filePath` | `string` | 文件的应用沙箱路径。 |
| `options?` | `any` | 支持如下选项： offset，number类型，表示期望读取文件的位置。可选，默认从当前位置开始读取。 length，number类型，表示期望读取数据的长度。可选，默认文件长度。 encoding，string类型，当数据是 string 类型时有效，表示数据的编码方式，默认 'utf-8'，仅支持 'utf-8'。 |

#### Returns

`string`

___

### write

▸ **write**(`fd`, `buffer`, `options?`): `Promise`\<`number`\>

将数据写入文件，使用Promise异步回调。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `fd` | `number` | number 已打开的文件描述符。 |
| `buffer` | `string` \| `ArrayBuffer` | ArrayBuffer\|string 待写入文件的数据，可来自缓冲区或字符串。 |
| `options?` | `any` | 支持如下选项： offset，number类型，表示期望写入文件的位置。可选，默认从当前位置开始写。 length，number类型，表示期望写入数据的长度。可选，默认缓冲区长度。 encoding，string类型，当数据是string类型时有效，表示数据的编码方式，默认 'utf-8'。当前仅支持 'utf-8'。 |

#### Returns

`Promise`\<`number`\>

___

### writeSync

▸ **writeSync**(`fd`, `buffer`, `options?`): `number`

将数据写入文件，以同步方法。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `fd` | `number` | number 已打开的文件描述符。 |
| `buffer` | `string` \| `ArrayBuffer` | ArrayBuffer\|string 待写入文件的数据，可来自缓冲区或字符串。 |
| `options?` | `any` | 支持如下选项： offset，number类型，表示期望写入文件的位置。可选，默认从当前位置开始写。 length，number类型，表示期望写入数据的长度。可选，默认缓冲区长度。 encoding，string类型，当数据是string类型时有效，表示数据的编码方式，默认 'utf-8'。当前仅支持 'utf-8'。 |

#### Returns

`number`

___

### writeEasy

▸ **writeEasy**(`path`, `buffer`, `append?`): `Promise`\<`number`\>

将数据写入文件，并关闭文件。

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `path` | `string` | `undefined` | string 文件的应用沙箱路径或URI。 |
| `buffer` | `string` \| `ArrayBuffer` | `undefined` | ArrayBuffer\|string 待写入文件的数据，可来自缓冲区或字符串。 |
| `append` | `boolean` | `true` | 是否追加，true-追加，false-不追加（直接覆盖） |

#### Returns

`Promise`\<`number`\>

___

### close

▸ **close**(`file`): `Promise`\<`void`\>

关闭文件，使用Promise异步回调。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `file` | `any` | 已打开的File对象或已打开的文件描述符fd。 |

#### Returns

`Promise`\<`void`\>

___

### closeSync

▸ **closeSync**(`file`): `void`

关闭文件，以同步方法。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `file` | `any` | 已打开的File对象或已打开的文件描述符fd。 |

#### Returns

`void`

___

### listFile

▸ **listFile**(`path`, `options?`): `Promise`\<`string`[]\>

列出文件夹下所有文件名，支持递归列出所有文件名（包含子目录下），支持文件过滤，使用Promise异步回调。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `path` | `string` | string 文件夹的应用沙箱路径。 |
| `options?` | `any` | 文件过滤选项。默认不进行过滤。 recursion boolean 是否递归子目录下文件名，默认为false。 listNum number 列出文件名数量。当设置0时，列出所有文件，默认为0。 filter Filter 文件过滤选项。当前仅支持后缀名匹配、文件名模糊查询、文件大小过滤、最近修改时间过滤。 |

#### Returns

`Promise`\<`string`[]\>

___

### listFileSync

▸ **listFileSync**(`path`, `options?`): `string`[]

列出文件夹下所有文件名，支持递归列出所有文件名（包含子目录下），支持文件过滤，以同步方法。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `path` | `string` | string 文件夹的应用沙箱路径。 |
| `options?` | `any` | 文件过滤选项。默认不进行过滤。 recursion boolean 是否递归子目录下文件名，默认为false。 listNum number 列出文件名数量。当设置0时，列出所有文件，默认为0。 filter Filter 文件过滤选项。当前仅支持后缀名匹配、文件名模糊查询、文件大小过滤、最近修改时间过滤。 |

#### Returns

`string`[]

___

### stat

▸ **stat**(`file`): `Promise`\<`Stat`\>

获取文件详细属性信息，使用Promise异步回调。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `file` | `string` \| `number` | string\|number 文件应用沙箱路径path或已打开的文件描述符fd。 |

#### Returns

`Promise`\<`Stat`\>

___

### statSync

▸ **statSync**(`file`): `Stat`

获取文件详细属性信息，以同步方法。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `file` | `string` \| `number` | string\|number 文件应用沙箱路径path或已打开的文件描述符fd。 |

#### Returns

`Stat`

___

### copy

▸ **copy**(`srcUri`, `destUri`, `options?`): `Promise`\<`void`\>

拷贝文件或者目录，支持拷贝进度监听，使用Promise异步返回。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `srcUri` | `string` | 待复制文件或目录的uri。 |
| `destUri` | `string` | 目标文件或目录的uri。 |
| `options?` | `any` | options中提供拷贝进度回调： ProgressListener 拷贝进度监听。 |

#### Returns

`Promise`\<`void`\>

___

### copyFile

▸ **copyFile**(`src`, `dest`, `mode?`): `Promise`\<`void`\>

复制文件，使用Promise异步回调。

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `src` | `string` \| `number` | `undefined` | string\|number 待复制文件的路径或待复制文件的文件描述符。 |
| `dest` | `string` \| `number` | `undefined` | string\|number 目标文件路径或目标文件的文件描述符。 |
| `mode` | `number` | `0` | number 提供覆盖文件的选项，当前仅支持0，且默认为0。0：完全覆盖目标文件。 |

#### Returns

`Promise`\<`void`\>

___

### copyFileSync

▸ **copyFileSync**(`src`, `dest`, `mode?`): `void`

以同步方法复制文件。

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `src` | `string` \| `number` | `undefined` | string\|number 待复制文件的路径或待复制文件的文件描述符。 |
| `dest` | `string` \| `number` | `undefined` | string\|number 目标文件路径或目标文件的文件描述符。 |
| `mode` | `number` | `0` | number 提供覆盖文件的选项，当前仅支持0，且默认为0。0：完全覆盖目标文件。 |

#### Returns

`void`

___

### copyDir

▸ **copyDir**(`src`, `dest`, `mode?`): `Promise`\<`void`\>

复制源文件夹至目标路径下，只能复制沙箱里的文件夹，使用Promise异步返回。

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `src` | `string` | `undefined` | 源文件夹的应用沙箱路径。 |
| `dest` | `string` | `undefined` | 目标文件夹的应用沙箱路径。 |
| `mode` | `number` | `1` | 复制模式: mode为0，文件级别抛异常。目标文件夹下存在与源文件夹名冲突的文件夹，若冲突文件夹下存在同名文件，则抛出异常。源文件夹下未冲突的文件全部移动至目标文件夹下，目标文件夹下未冲突文件将继续保留，且冲突文件信息将在抛出异常的data属性中以Array<ConflictFiles>形式提供。 mode为1，文件级别强制覆盖。目标文件夹下存在与源文件夹名冲突的文件夹，若冲突文件夹下存在同名文件，则强制覆盖冲突文件夹下所有同名文件，未冲突文件将继续保留。 |

#### Returns

`Promise`\<`void`\>

___

### copyDirSync

▸ **copyDirSync**(`src`, `dest`, `mode?`): `void`

以同步方法复制源文件夹至目标路径下，只能复制沙箱里的文件夹。

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `src` | `string` | `undefined` | 源文件夹的应用沙箱路径。 |
| `dest` | `string` | `undefined` | 目标文件夹的应用沙箱路径。 |
| `mode` | `number` | `1` | 复制模式: mode为0，文件级别抛异常。目标文件夹下存在与源文件夹名冲突的文件夹，若冲突文件夹下存在同名文件，则抛出异常。源文件夹下未冲突的文件全部移动至目标文件夹下，目标文件夹下未冲突文件将继续保留，且冲突文件信息将在抛出异常的data属性中以Array<ConflictFiles>形式提供。 mode为1，文件级别强制覆盖。目标文件夹下存在与源文件夹名冲突的文件夹，若冲突文件夹下存在同名文件，则强制覆盖冲突文件夹下所有同名文件，未冲突文件将继续保留。 |

#### Returns

`void`

___

### moveFile

▸ **moveFile**(`src`, `dest`, `mode?`): `Promise`\<`void`\>

移动文件，使用Promise异步回调。

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `src` | `string` | `undefined` | string 源文件的应用沙箱路径。 |
| `dest` | `string` | `undefined` | string 目的文件的应用沙箱路径。 |
| `mode` | `number` | `0` | number 移动模式。若mode为0，移动位置存在同名文件时，强制移动覆盖。若mode为1，移动位置存在同名文件时，抛出异常。默认为0。 |

#### Returns

`Promise`\<`void`\>

___

### moveFileSync

▸ **moveFileSync**(`src`, `dest`, `mode?`): `void`

移动文件，以同步方法。

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `src` | `string` | `undefined` | string 源文件的应用沙箱路径。 |
| `dest` | `string` | `undefined` | string 目的文件的应用沙箱路径。 |
| `mode` | `number` | `0` | number 移动模式。若mode为0，移动位置存在同名文件时，强制移动覆盖。若mode为1，移动位置存在同名文件时，抛出异常。默认为0。 |

#### Returns

`void`

___

### moveDir

▸ **moveDir**(`src`, `dest`, `mode?`): `Promise`\<`void`\>

移动源文件夹至目标路径下，使用Promise异步返回。

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `src` | `string` | `undefined` | 源文件夹的应用沙箱路径 |
| `dest` | `string` | `undefined` | 目标文件夹的应用沙箱路径 |
| `mode` | `number` | `3` | 移动模式: mode为0，文件夹级别抛异常。若目标文件夹下存在与源文件夹名冲突的非空文件夹，则抛出异常。 mode为1，文件级别抛异常。目标文件夹下存在与源文件夹名冲突的文件夹，若冲突文件夹下存在同名文件，则抛出异常。源文件夹下未冲突的文件全部移动至目标文件夹下，目标文件夹下未冲突文件将继续保留，且冲突文件信息将在抛出异常的data属性中以Array<ConflictFiles>形式提供。 mode为2，文件级别强制覆盖。目标文件夹下存在与源文件夹名冲突的文件夹，若冲突文件夹下存在同名文件，则强制覆盖冲突文件夹下所有同名文件，未冲突文件将继续保留。 mode为3，文件夹级别强制覆盖。移动源文件夹至目标文件夹下，目标文件夹下移动的文件夹内容与源文件夹完全一致。若目标文件夹下存在与源文件夹名冲突的文件夹，该文件夹下所有原始文件将不会保留。 |

#### Returns

`Promise`\<`void`\>

___

### moveDirSync

▸ **moveDirSync**(`src`, `dest`, `mode?`): `any`

以同步方法移动源文件夹至目标路径下。

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `src` | `string` | `undefined` | 源文件夹的应用沙箱路径 |
| `dest` | `string` | `undefined` | 目标文件夹的应用沙箱路径 |
| `mode` | `number` | `3` | 移动模式: mode为0，文件夹级别抛异常。若目标文件夹下存在与源文件夹名冲突的非空文件夹，则抛出异常。 mode为1，文件级别抛异常。目标文件夹下存在与源文件夹名冲突的文件夹，若冲突文件夹下存在同名文件，则抛出异常。源文件夹下未冲突的文件全部移动至目标文件夹下，目标文件夹下未冲突文件将继续保留，且冲突文件信息将在抛出异常的data属性中以Array<ConflictFiles>形式提供。 mode为2，文件级别强制覆盖。目标文件夹下存在与源文件夹名冲突的文件夹，若冲突文件夹下存在同名文件，则强制覆盖冲突文件夹下所有同名文件，未冲突文件将继续保留。 mode为3，文件夹级别强制覆盖。移动源文件夹至目标文件夹下，目标文件夹下移动的文件夹内容与源文件夹完全一致。若目标文件夹下存在与源文件夹名冲突的文件夹，该文件夹下所有原始文件将不会保留。 |

#### Returns

`any`

___

### truncate

▸ **truncate**(`file`, `len?`): `Promise`\<`void`\>

截断文件，使用Promise异步回调。

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `file` | `string` \| `number` | `undefined` | string\|number 文件的应用沙箱路径或已打开的文件描述符fd。 |
| `len` | `number` | `0` | number 文件截断后的长度，以字节为单位。默认为0。 |

#### Returns

`Promise`\<`void`\>

___

### truncateSync

▸ **truncateSync**(`file`, `len?`): `void`

截断文件，以同步方法。

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `file` | `string` \| `number` | `undefined` | string\|number 文件的应用沙箱路径或已打开的文件描述符fd。 |
| `len` | `number` | `0` | number 文件截断后的长度，以字节为单位。默认为0。 |

#### Returns

`void`

___

### lstat

▸ **lstat**(`path`): `Promise`\<`Stat`\>

获取链接文件信息，使用Promise异步回调。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `path` | `string` | string 文件的应用沙箱路径。 |

#### Returns

`Promise`\<`Stat`\>

___

### lstatSync

▸ **lstatSync**(`path`): `Stat`

获取链接文件信息，以同步方法。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `path` | `string` | string 文件的应用沙箱路径。 |

#### Returns

`Stat`

___

### fsync

▸ **fsync**(`fd`): `Promise`\<`void`\>

同步文件数据，使用Promise异步回调。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `fd` | `number` | number 已打开的文件描述符。 |

#### Returns

`Promise`\<`void`\>

___

### fsyncSync

▸ **fsyncSync**(`fd`): `void`

同步文件数据，以同步方法。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `fd` | `number` | number 已打开的文件描述符。 |

#### Returns

`void`

___

### fdatasync

▸ **fdatasync**(`fd`): `Promise`\<`void`\>

实现文件内容数据同步，使用Promise异步回调。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `fd` | `number` | number 已打开的文件描述符。 |

#### Returns

`Promise`\<`void`\>

___

### fdatasyncSync

▸ **fdatasyncSync**(`fd`): `void`

实现文件内容数据同步，以同步方法。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `fd` | `number` | number 已打开的文件描述符。 |

#### Returns

`void`

___

### createStream

▸ **createStream**(`path`, `mode?`): `Promise`\<`Stream`\>

基于文件路径打开文件流，使用Promise异步回调。

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `path` | `string` | `undefined` | string 文件的应用沙箱路径。 |
| `mode` | `string` | `'r'` | string 文件打开类型 r：打开只读文件，该文件必须存在。 r+：打开可读写的文件，该文件必须存在。 w：打开只写文件，若文件存在则文件长度清0，即该文件内容会消失。若文件不存在则建立该文件。 w+：打开可读写文件，若文件存在则文件长度清0，即该文件内容会消失。若文件不存在则建立该文件。 a：以附加的方式打开只写文件。若文件不存在，则会建立该文件，如果文件存在，写入的数据会被加到文件尾，即文件原先的内容会被保留。 a+：以附加方式打开可读写的文件。若文件不存在，则会建立该文件，如果文件存在，写入的数据会被加到文件尾后，即文件原先的内容会被保留。 |

#### Returns

`Promise`\<`Stream`\>

___

### createStreamSync

▸ **createStreamSync**(`path`, `mode?`): `Stream`

基于文件路径打开文件流，以同步方法。

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `path` | `string` | `undefined` | string 文件的应用沙箱路径。 |
| `mode` | `string` | `'r'` | string 文件打开类型 r：打开只读文件，该文件必须存在。 r+：打开可读写的文件，该文件必须存在。 w：打开只写文件，若文件存在则文件长度清0，即该文件内容会消失。若文件不存在则建立该文件。 w+：打开可读写文件，若文件存在则文件长度清0，即该文件内容会消失。若文件不存在则建立该文件。 a：以附加的方式打开只写文件。若文件不存在，则会建立该文件，如果文件存在，写入的数据会被加到文件尾，即文件原先的内容会被保留。 a+：以附加方式打开可读写的文件。若文件不存在，则会建立该文件，如果文件存在，写入的数据会被加到文件尾后，即文件原先的内容会被保留。 |

#### Returns

`Stream`

___

### fdopenStream

▸ **fdopenStream**(`fd`, `mode?`): `Promise`\<`Stream`\>

基于文件描述符打开文件流，使用Promise异步回调。

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `fd` | `number` | `undefined` | number 已打开的文件描述符。 |
| `mode` | `string` | `'r'` | string 文件打开类型 r：打开只读文件，该文件必须存在。 r+：打开可读写的文件，该文件必须存在。 w：打开只写文件，若文件存在则文件长度清0，即该文件内容会消失。若文件不存在则建立该文件。 w+：打开可读写文件，若文件存在则文件长度清0，即该文件内容会消失。若文件不存在则建立该文件。 a：以附加的方式打开只写文件。若文件不存在，则会建立该文件，如果文件存在，写入的数据会被加到文件尾，即文件原先的内容会被保留。 a+：以附加方式打开可读写的文件。若文件不存在，则会建立该文件，如果文件存在，写入的数据会被加到文件尾后，即文件原先的内容会被保留。 |

#### Returns

`Promise`\<`Stream`\>

___

### fdopenStreamSync

▸ **fdopenStreamSync**(`fd`, `mode?`): `Stream`

基于文件描述符打开文件流，以同步方法。

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `fd` | `number` | `undefined` | number 已打开的文件描述符。 |
| `mode` | `string` | `'r'` | string 文件打开类型 r：打开只读文件，该文件必须存在。 r+：打开可读写的文件，该文件必须存在。 w：打开只写文件，若文件存在则文件长度清0，即该文件内容会消失。若文件不存在则建立该文件。 w+：打开可读写文件，若文件存在则文件长度清0，即该文件内容会消失。若文件不存在则建立该文件。 a：以附加的方式打开只写文件。若文件不存在，则会建立该文件，如果文件存在，写入的数据会被加到文件尾，即文件原先的内容会被保留。 a+：以附加方式打开可读写的文件。若文件不存在，则会建立该文件，如果文件存在，写入的数据会被加到文件尾后，即文件原先的内容会被保留。 |

#### Returns

`Stream`

___

### mkdtemp

▸ **mkdtemp**(`prefix`): `Promise`\<`string`\>

创建临时目录，使用Promise异步回调。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `prefix` | `string` | string 用随机产生的字符串替换以“XXXXXX”结尾目录路径。 |

#### Returns

`Promise`\<`string`\>

___

### mkdtempSync

▸ **mkdtempSync**(`prefix`): `string`

创建临时目录，以同步的方法。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `prefix` | `string` | string 用随机产生的字符串替换以“XXXXXX”结尾目录路径。 |

#### Returns

`string`

___

### dup

▸ **dup**(`fd`): `File`

将文件描述符转化为File。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `fd` | `number` | 文件描述符。 |

#### Returns

`File`

___

### utimes

▸ **utimes**(`path`, `mtime`): `void`

修改文件最近访问时间属性。
path 文件的应用沙箱路径。
mtime 待更新的时间戳。自1970年1月1日起至目标时间的毫秒数。仅支持修改文件最近访问时间属性。

#### Parameters

| Name | Type |
| :------ | :------ |
| `path` | `string` |
| `mtime` | `number` |

#### Returns

`void`

___

### getFormatFileSize

▸ **getFormatFileSize**(`fileSize`): `string`

格式化文件大小

#### Parameters

| Name | Type |
| :------ | :------ |
| `fileSize` | `number` |

#### Returns

`string`

___

### getRawFileContentSync

▸ **getRawFileContentSync**(`path`): `Uint8Array`

获取resources/rawfile目录下对应的rawfile文件内容，使用同步形式返回

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `path` | `string` | rawfile文件路径 |

#### Returns

`Uint8Array`

___

### getRawFileContent

▸ **getRawFileContent**(`path`): `Promise`\<`Uint8Array`\>

获取resources/rawfile目录下对应的rawfile文件内容，使用Promise异步回调

#### Parameters

| Name | Type |
| :------ | :------ |
| `path` | `string` |

#### Returns

`Promise`\<`Uint8Array`\>

___

### getRawFileContentStrSync

▸ **getRawFileContentStrSync**(`path`): `string`

获取resources/rawfile目录下对应的rawfile文件内容，使用同步形式返回

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `path` | `string` | rawfile文件路径 |

#### Returns

`string`

___

### getRawFileContentStr

▸ **getRawFileContentStr**(`path`): `Promise`\<`string`\>

获取resources/rawfile目录下对应的rawfile文件内容，使用Promise异步回调

#### Parameters

| Name | Type |
| :------ | :------ |
| `path` | `string` |

#### Returns

`Promise`\<`string`\>

___

### saveImage

▸ **saveImage**(`pixelMap`, `dirPath?`, `fileName`, `quality?`): `Promise`\<`string`\>

将PixelMap图像数据保存到本地沙盒目录

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `pixelMap` | `PixelMap` | `undefined` | PixelMap图像数据 |
| `dirPath` | `string` | `"images"` | 保存目录路径，相对沙盒目录 |
| `fileName` | `string` | `undefined` | 保存的文件名（包含扩展名） |
| `quality` | `number` | `80` | 图片质量，1-100，默认80 |

#### Returns

`Promise`\<`string`\>

保存后的文件完整路径
