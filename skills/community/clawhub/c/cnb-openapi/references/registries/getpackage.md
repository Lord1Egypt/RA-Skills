# GetPackage

## 原始 Swagger
https://api.cnb.cool/#/operations/GetPackage

## 接口描述
获取指定制品的详细信息。 Get the package detail.
## 接口权限
registry-package:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{slug}/-/packages/{type}/{name}

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| slug | 字符串 | 是 | 资源路径。Slug.|
| t | 字符串 | 是 | 制品类型。Type|
| name | 字符串 | 是 | 制品名称。Name|
## 响应信息


**响应类型：** dto.PackageDetail

**响应结构：**
```json
{
  "cargo": {
    "address": "string",
    "desc": "string",
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
    "slug": "string",
    "tag_total": 0,
    "tags": [{
      "desc": "string",
      "digest": "string",
      "has_provenance": false,
      "last_pusher": {
        "is_frozen": false,
        "is_lock": false,
        "name": "string",
        "nickname": "string",
        "push_at": "string"
      },
      "name": "string",
      "pull_count": 0,
      "recent_pull_count": 0,
      "size": 0,
      "status": "string"
    }]
  },
  "composer": {
    "address": "string",
    "desc": "string",
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
    "slug": "string",
    "tag_total": 0,
    "tags": [{
      "desc": "string",
      "digest": "string",
      "has_provenance": false,
      "last_pusher": {
        "is_frozen": false,
        "is_lock": false,
        "name": "string",
        "nickname": "string",
        "push_at": "string"
      },
      "name": "string",
      "pull_count": 0,
      "recent_pull_count": 0,
      "size": 0,
      "status": "string"
    }]
  },
  "conan": {
    "address": "string",
    "desc": "string",
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
    "slug": "string",
    "tag_total": 0,
    "tags": [{
      "desc": "string",
      "digest": "string",
      "has_provenance": false,
      "last_pusher": {
        "is_frozen": false,
        "is_lock": false,
        "name": "string",
        "nickname": "string",
        "push_at": "string"
      },
      "name": "string",
      "pull_count": 0,
      "recent_pull_count": 0,
      "size": 0,
      "status": "string"
    }]
  },
  "docker": {
    "address": "string",
    "desc": "string",
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
    "slug": "string",
    "tag_total": 0,
    "tags": [{
      "address": "string",
      "annotations": {
        "revision": "string",
        "sn": "string",
        "version": "string"
      },
      "git_address": "string",
      "has_provenance": false,
      "images": [{
        "arch": "string",
        "digest": "string",
        "layers": [{
          "instruction": "string",
          "size": 0
        }],
        "os": "string",
        "size": 0
      }],
      "last_pusher": {
        "is_frozen": false,
        "is_lock": false,
        "name": "string",
        "nickname": "string",
        "push_at": "string"
      },
      "name": "string",
      "pull_count": 0,
      "recent_pull_count": 0,
      "type": "string"
    }]
  },
  "dockermodel": {
    "address": "string",
    "desc": "string",
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
    "slug": "string",
    "tag_total": 0,
    "tags": [{
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
      "git_address": "string",
      "has_provenance": false,
      "last_pusher": {
        "is_frozen": false,
        "is_lock": false,
        "name": "string",
        "nickname": "string",
        "push_at": "string"
      },
      "name": "string",
      "pull_count": 0,
      "recent_pull_count": 0,
      "size": 0
    }]
  },
  "generic": {
    "address": "string",
    "desc": "string",
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
    "slug": "string",
    "tag_total": 0,
    "tags": [{
      "desc": "string",
      "digest": "string",
      "has_provenance": false,
      "last_pusher": {
        "is_frozen": false,
        "is_lock": false,
        "name": "string",
        "nickname": "string",
        "push_at": "string"
      },
      "name": "string",
      "pull_count": 0,
      "recent_pull_count": 0,
      "size": 0,
      "status": "string"
    }]
  },
  "helm": {
    "address": "string",
    "desc": "string",
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
    "slug": "string",
    "tag_total": 0,
    "tags": [{
      "address": "string",
      "digest": "string",
      "git_address": "string",
      "has_provenance": false,
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
      "name": "string",
      "pull_count": 0,
      "recent_pull_count": 0,
      "size": 0
    }]
  },
  "maven": {
    "address": "string",
    "desc": "string",
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
    "slug": "string",
    "tag_total": 0,
    "tags": [{
      "desc": "string",
      "digest": "string",
      "has_provenance": false,
      "last_pusher": {
        "is_frozen": false,
        "is_lock": false,
        "name": "string",
        "nickname": "string",
        "push_at": "string"
      },
      "name": "string",
      "pull_count": 0,
      "recent_pull_count": 0,
      "size": 0,
      "status": "string"
    }]
  },
  "npm": {
    "address": "string",
    "desc": "string",
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
    "slug": "string",
    "tag_total": 0,
    "tags": [{
      "desc": "string",
      "digest": "string",
      "has_provenance": false,
      "last_pusher": {
        "is_frozen": false,
        "is_lock": false,
        "name": "string",
        "nickname": "string",
        "push_at": "string"
      },
      "name": "string",
      "pull_count": 0,
      "recent_pull_count": 0,
      "size": 0,
      "status": "string"
    }]
  },
  "nuget": {
    "address": "string",
    "desc": "string",
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
    "slug": "string",
    "tag_total": 0,
    "tags": [{
      "desc": "string",
      "digest": "string",
      "has_provenance": false,
      "last_pusher": {
        "is_frozen": false,
        "is_lock": false,
        "name": "string",
        "nickname": "string",
        "push_at": "string"
      },
      "name": "string",
      "pull_count": 0,
      "recent_pull_count": 0,
      "size": 0,
      "status": "string"
    }]
  },
  "ohpm": {
    "address": "string",
    "desc": "string",
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
    "slug": "string",
    "tag_total": 0,
    "tags": [{
      "desc": "string",
      "digest": "string",
      "has_provenance": false,
      "last_pusher": {
        "is_frozen": false,
        "is_lock": false,
        "name": "string",
        "nickname": "string",
        "push_at": "string"
      },
      "name": "string",
      "pull_count": 0,
      "recent_pull_count": 0,
      "size": 0,
      "status": "string"
    }]
  },
  "pypi": {
    "address": "string",
    "desc": "string",
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
    "slug": "string",
    "tag_total": 0,
    "tags": [{
      "desc": "string",
      "digest": "string",
      "has_provenance": false,
      "last_pusher": {
        "is_frozen": false,
        "is_lock": false,
        "name": "string",
        "nickname": "string",
        "push_at": "string"
      },
      "name": "string",
      "pull_count": 0,
      "recent_pull_count": 0,
      "size": 0,
      "status": "string"
    }]
  }
}
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{slug}/-/packages/{type}/{name}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
```
