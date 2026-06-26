# GetPackageTagDetail

## 原始 Swagger
https://api.cnb.cool/#/operations/GetPackageTagDetail

## 接口描述
获取制品标签详情。 Get the specific tag under specific package.
## 接口权限
registry-package:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{slug}/-/packages/{type}/{name}/-/tag/{tag}

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| slug | 字符串 | 是 | Slug|
| t | 字符串 | 是 | Type|
| name | 字符串 | 是 | Name|
| tag | 字符串 | 是 | Tag|

### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| sha256 | 字符串 | 否| 摘要|
| arch | 字符串 | 否| 架构，docker制品必需，例: linux/amd64/v3。required for docker artifacts|
## 响应信息


**响应类型：** dto.TagDetail

**响应结构：**
```json
{
  "cargo": {
    "address": "string",
    "dependencies": [{
      "artifact": "string",
      "framework_name": "string",
      "name": "string"
    }],
    "desc": "string",
    "files": [{
      "name": "string",
      "size": 0
    }],
    "has_provenance": false, // HasProvenance 是否有出生证明; pypi和conan制品由于有多架构，取决于最新推送.
    "last_pusher": {
      "is_frozen": false,
      "is_lock": false,
      "name": "string",
      "nickname": "string",
      "push_at": "string"
    },
    "metadata": {
      "author": "string",
      "home_page": "string",
      "license_url": "string",
      "package_name": "string",
      "package_tag": "string",
      "package_type": "string",
      "readme": "string",
      "repository_url": "string"
    },
    "package": "string",
    "pull_count": 0,
    "recent_pull_count": 0,
    "size": 0,
    "slug": "string",
    "status": "string",
    "tag": "string"
  },
  "composer": {
    "address": "string",
    "dependencies": [{
      "artifact": "string",
      "framework_name": "string",
      "name": "string"
    }],
    "desc": "string",
    "files": [{
      "name": "string",
      "size": 0
    }],
    "has_provenance": false, // HasProvenance 是否有出生证明; pypi和conan制品由于有多架构，取决于最新推送.
    "last_pusher": {
      "is_frozen": false,
      "is_lock": false,
      "name": "string",
      "nickname": "string",
      "push_at": "string"
    },
    "metadata": {
      "author": "string",
      "home_page": "string",
      "license_url": "string",
      "package_name": "string",
      "package_tag": "string",
      "package_type": "string",
      "readme": "string",
      "repository_url": "string"
    },
    "package": "string",
    "pull_count": 0,
    "recent_pull_count": 0,
    "size": 0,
    "slug": "string",
    "status": "string",
    "tag": "string"
  },
  "conan": {
    "address": "string",
    "dependencies": [{
      "artifact": "string",
      "framework_name": "string",
      "name": "string"
    }],
    "desc": "string",
    "files": [{
      "name": "string",
      "size": 0
    }],
    "has_provenance": false, // HasProvenance 是否有出生证明; pypi和conan制品由于有多架构，取决于最新推送.
    "last_pusher": {
      "is_frozen": false,
      "is_lock": false,
      "name": "string",
      "nickname": "string",
      "push_at": "string"
    },
    "metadata": {
      "author": "string",
      "conan_packages": [{
        "arch": "string",
        "build_type": "string",
        "compiler": {},
        "options": {},
        "os": "string",
        "package_id": "string",
        "package_revision": "string",
        "requires": ["string"]
      }], // conan 的 package 列表
      "conan_recipe_revision": "string", // conan recipe 的 revision, conan 制品专用字段
      "conan_reference": "string",
      "home_page": "string",
      "license_url": "string",
      "package_name": "string",
      "package_tag": "string",
      "package_type": "string",
      "readme": "string",
      "repository_url": "string"
    },
    "package": "string",
    "pull_count": 0,
    "recent_pull_count": 0,
    "size": 0,
    "slug": "string",
    "status": "string",
    "tag": "string"
  },
  "docker": {
    "address": "string",
    "annotations": {
      "revision": "string",
      "sn": "string",
      "version": "string"
    },
    "git_address": "string", // 源仓库地址
    "has_provenance": false, // HasProvenance 是否有出生证明; pypi和conan制品由于有多架构，取决于最新推送.
    "image": {
      "arch": "string",
      "digest": "string",
      "layers": [{
        "instruction": "string",
        "size": 0
      }],
      "os": "string",
      "size": 0
    },
    "last_pusher": {
      "is_frozen": false,
      "is_lock": false,
      "name": "string",
      "nickname": "string",
      "push_at": "string"
    },
    "matches_requested_arch": false, // 返回的结果是否和提供的架构匹配
    "options": [{
      "arch": "string",
      "digest": "string",
      "layers": [{
        "instruction": "string",
        "size": 0
      }],
      "os": "string",
      "size": 0
    }],
    "package": "string",
    "pull_count": 0,
    "recent_pull_count": 0,
    "slug": "string",
    "tag": "string",
    "type": "string"
  },
  "dockermodel": {
    "address": "string",
    "config": {
      "architecture": "string",
      "format": "string", // Format the packaging format of the model file(s), currently the only supported value is gguf.
      "format_version": "string", // FormatVersion the version of the format
      "gguf": {
      },
      "parameters": "string",
      "quantization": "string",
      "size": "string"
    },
    "descriptor": {
      "created": "string"
    },
    "git_address": "string", // 源仓库地址
    "has_provenance": false, // HasProvenance 是否有出生证明; pypi和conan制品由于有多架构，取决于最新推送.
    "last_pusher": {
      "is_frozen": false,
      "is_lock": false,
      "name": "string",
      "nickname": "string",
      "push_at": "string"
    },
    "package": "string",
    "pull_count": 0,
    "recent_pull_count": 0,
    "size": 0,
    "slug": "string",
    "tag": "string"
  },
  "generic": {
    "address": "string",
    "dependencies": [{
      "artifact": "string",
      "framework_name": "string",
      "name": "string"
    }],
    "desc": "string",
    "files": [{
      "name": "string",
      "size": 0
    }],
    "has_provenance": false, // HasProvenance 是否有出生证明; pypi和conan制品由于有多架构，取决于最新推送.
    "last_pusher": {
      "is_frozen": false,
      "is_lock": false,
      "name": "string",
      "nickname": "string",
      "push_at": "string"
    },
    "metadata": {
      "author": "string",
      "home_page": "string",
      "license_url": "string",
      "package_name": "string",
      "package_tag": "string",
      "package_type": "string",
      "readme": "string",
      "repository_url": "string"
    },
    "package": "string",
    "pull_count": 0,
    "recent_pull_count": 0,
    "size": 0,
    "slug": "string",
    "status": "string",
    "tag": "string"
  },
  "helm": {
    "address": "string",
    "git_address": "string", // 源仓库地址
    "has_provenance": false, // HasProvenance 是否有出生证明; pypi和conan制品由于有多架构，取决于最新推送.
    "is_deprecated": false,
    "last_pusher": {
      "is_frozen": false,
      "is_lock": false,
      "name": "string",
      "nickname": "string",
      "push_at": "string"
    },
    "metadata": {
      "annotations": {}, // Annotations are additional mappings uninterpreted by Helm,
made available for inspection by other applications.
      "apiVersion": "string", // The API Version of this chart. Required.
      "appVersion": "string", // The version of the application enclosed inside of this chart.
      "condition": "string", // The condition to check to enable chart
      "dependencies": [{
        "alias": "string", // Alias usable alias to be used for the chart
        "condition": "string", // A yaml path that resolves to a boolean, used for enabling/disabling charts (e.g. subchart1.enabled )
        "enabled": false, // Enabled bool determines if chart should be loaded
        "import-values": [null], // ImportValues holds the mapping of source values to parent key to be imported. Each item can be a
string or pair of child/parent sublist items.
        "name": "string", // Name is the name of the dependency.

This must mach the name in the dependency's Chart.yaml.
        "repository": "string", // The URL to the repository.

Appending `index.yaml` to this string should result in a URL that can be
used to fetch the repository index.
        "tags": ["string"], // Tags can be used to group charts for enabling/disabling together
        "version": "string" // Version is the version (range) of this chart.

A lock file will always produce a single version, while a dependency
may contain a semantic version range.
      }], // Dependencies are a list of dependencies for a chart.
      "deprecated": false, // Whether or not this chart is deprecated
      "description": "string", // A one-sentence description of the chart
      "home": "string", // The URL to a relevant project page, git repo, or contact person
      "icon": "string", // The URL to an icon file.
      "keywords": ["string"], // A list of string keywords
      "kubeVersion": "string", // KubeVersion is a SemVer constraint specifying the version of Kubernetes required.
      "maintainers": [{
        "email": "string", // Email is an optional email address to contact the named maintainer
        "name": "string", // Name is a user name or organization name
        "url": "string" // URL is an optional URL to an address for the named maintainer
      }], // A list of name and URL/email address combinations for the maintainer(s)
      "name": "string", // The name of the chart. Required.
      "sources": ["string"], // Source is the URL to the source code of this chart
      "tags": "string", // The tags to check to enable chart
      "type": "string", // Specifies the chart type: application or library
      "version": "string" // A SemVer 2 conformant version string of the chart. Required.
    },
    "package": "string",
    "pull_count": 0,
    "recent_pull_count": 0,
    "size": 0,
    "slug": "string",
    "tag": "string"
  },
  "maven": {
    "address": "string",
    "dependencies": [{
      "artifact": "string",
      "framework_name": "string",
      "name": "string"
    }],
    "desc": "string",
    "files": [{
      "name": "string",
      "size": 0
    }],
    "has_provenance": false, // HasProvenance 是否有出生证明; pypi和conan制品由于有多架构，取决于最新推送.
    "last_pusher": {
      "is_frozen": false,
      "is_lock": false,
      "name": "string",
      "nickname": "string",
      "push_at": "string"
    },
    "metadata": {
      "author": "string",
      "home_page": "string",
      "license_url": "string",
      "package_name": "string",
      "package_tag": "string",
      "package_type": "string",
      "readme": "string",
      "repository_url": "string"
    },
    "package": "string",
    "pull_count": 0,
    "recent_pull_count": 0,
    "size": 0,
    "slug": "string",
    "status": "string",
    "tag": "string"
  },
  "npm": {
    "address": "string",
    "dependencies": [{
      "artifact": "string",
      "framework_name": "string",
      "name": "string"
    }],
    "desc": "string",
    "files": [{
      "name": "string",
      "size": 0
    }],
    "has_provenance": false, // HasProvenance 是否有出生证明; pypi和conan制品由于有多架构，取决于最新推送.
    "last_pusher": {
      "is_frozen": false,
      "is_lock": false,
      "name": "string",
      "nickname": "string",
      "push_at": "string"
    },
    "metadata": {
      "author": "string",
      "home_page": "string",
      "license_url": "string",
      "package_name": "string",
      "package_tag": "string",
      "package_type": "string",
      "readme": "string",
      "repository_url": "string"
    },
    "package": "string",
    "pull_count": 0,
    "recent_pull_count": 0,
    "size": 0,
    "slug": "string",
    "status": "string",
    "tag": "string"
  },
  "nuget": {
    "address": "string",
    "dependencies": [{
      "artifact": "string",
      "framework_name": "string",
      "name": "string"
    }],
    "desc": "string",
    "files": [{
      "name": "string",
      "size": 0
    }],
    "has_provenance": false, // HasProvenance 是否有出生证明; pypi和conan制品由于有多架构，取决于最新推送.
    "last_pusher": {
      "is_frozen": false,
      "is_lock": false,
      "name": "string",
      "nickname": "string",
      "push_at": "string"
    },
    "metadata": {
      "author": "string",
      "home_page": "string",
      "license_url": "string",
      "package_name": "string",
      "package_tag": "string",
      "package_type": "string",
      "readme": "string",
      "repository_url": "string"
    },
    "package": "string",
    "pull_count": 0,
    "recent_pull_count": 0,
    "size": 0,
    "slug": "string",
    "status": "string",
    "tag": "string"
  },
  "ohpm": {
    "address": "string",
    "dependencies": [{
      "artifact": "string",
      "framework_name": "string",
      "name": "string"
    }],
    "desc": "string",
    "files": [{
      "name": "string",
      "size": 0
    }],
    "has_provenance": false, // HasProvenance 是否有出生证明; pypi和conan制品由于有多架构，取决于最新推送.
    "last_pusher": {
      "is_frozen": false,
      "is_lock": false,
      "name": "string",
      "nickname": "string",
      "push_at": "string"
    },
    "metadata": {
      "author": "string",
      "home_page": "string",
      "license_url": "string",
      "package_name": "string",
      "package_tag": "string",
      "package_type": "string",
      "readme": "string",
      "repository_url": "string"
    },
    "package": "string",
    "pull_count": 0,
    "recent_pull_count": 0,
    "size": 0,
    "slug": "string",
    "status": "string",
    "tag": "string"
  },
  "pypi": {
    "address": "string",
    "dependencies": [{
      "artifact": "string",
      "framework_name": "string",
      "name": "string"
    }],
    "desc": "string",
    "files": [{
      "name": "string",
      "size": 0
    }],
    "has_provenance": false, // HasProvenance 是否有出生证明; pypi和conan制品由于有多架构，取决于最新推送.
    "last_pusher": {
      "is_frozen": false,
      "is_lock": false,
      "name": "string",
      "nickname": "string",
      "push_at": "string"
    },
    "metadata": {
      "author": "string",
      "home_page": "string",
      "license_url": "string",
      "minimum_stability": "string",
      "package_name": "string",
      "package_tag": "string",
      "package_type": "string",
      "readme": "string",
      "repository_url": "string"
    },
    "package": "string",
    "pull_count": 0,
    "recent_pull_count": 0,
    "size": 0,
    "slug": "string",
    "status": "string",
    "tag": "string"
  }
}
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{slug}/-/packages/{type}/{name}/-/tag/{tag}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
-G \
-d "sha256=<sha256>" \
-d "arch=<arch>" \
```
