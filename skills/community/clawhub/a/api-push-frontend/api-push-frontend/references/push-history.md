# API 推送历史记录


## 2026-04-09 19:26:20

- **时间**: 2026-04-09 19:26:20
- **prdId**: PRD_20260408_185353_1A679C6F7A
- **接口数量**: 6
- **状态**: ❌ 失败
- **响应**: ```json
{
  "error": "网络错误",
  "message": "timed out"
}
```

---
# API 推送历史记录


## 2026-04-09 19:10:09

- **时间**: 2026-04-09 19:10:09
- **prdId**: PRD_20260408_185353_1A679C6F7A
- **接口数量**: 6
- **状态**: ❌ 失败
- **响应**: ```json
{
  "error": "网络错误",
  "message": "timed out"
}
```

---
# API 推送历史记录


## 2026-04-09 19:07:05

- **时间**: 2026-04-09 19:07:05
- **prdId**: PRD_20260408_185353_1A679C6F7A
- **接口数量**: 6
- **状态**: ❌ 失败
- **响应**: ```json
{
  "error": "网络错误",
  "message": "timed out"
}
```

---
# API 推送历史记录


## 2026-04-01 20:41:46

- **时间**: 2026-04-01 20:41:46
- **prdId**: PRD_20260401_202428_AN60GPOF
- **接口数量**: 8
- **状态**: ✅ 成功
- **响应**: ```json
{
  "success": true,
  "prdId": "PRD_20260401_202428_AN60GPOF",
  "prdName": "小程序转发作品数据统计_20260331180000",
  "apis": [
    {
      "module": "配置管理",
      "moduleCode": "config",
      "controller": "ConfigManageController",
      "endpoints": [
        {
          "id": "config-001",
          "name": "分页查询配置列表",
          "method": "GET",
          "path": "/v1.0/system/config/configs/page",
          "params": [
            "pageNum",
            "pageSize",
            "configTitle",
            "configType",
            "status"
          ],
          "response": "PageInfo<ConfigManageVo>"
        },
        {
          "id": "config-002",
          "name": "查询配置列表",
          "method": "GET",
          "path": "/v1.0/system/config/configs/list",
          "params": [],
          "response": "List<ConfigManageVo>"
        },
        {
          "id": "config-003",
          "name": "根据 ID 查询配置",
          "method": "GET",
          "path": "/v1.0/system/config/configs/{id}",
          "params": [
            "id"
          ],
          "response": "ConfigManageVo"
        },
        {
          "id": "config-004",
          "name": "新增配置",
          "method": "POST",
          "path": "/v1.0/system/config/configs",
          "params": [
            "configTitle",
            "configContent",
            "configType",
            "description",
            "sort",
            "status"
          ],
          "response": "void"
        },
        {
          "id": "config-005",
          "name": "修改配置",
          "method": "POST",
          "path": "/v1.0/system/config/configs/update",
          "params": [
            "id",
            "configTitle",
            "configContent",
            "configType",
            "description",
            "sort",
            "status"
          ],
          "response": "void"
        },
        {
          "id": "config-006",
          "name": "删除配置",
          "method": "DELETE",
          "path": "/v1.0/system/config/configs/{id}",
          "params": [
            "id"
          ],
          "response": "void"
        }
      ]
    },
    {
      "module": "环境管理",
      "moduleCode": "environment",
      "controller": "DevEnvironmentController",
      "endpoints": [
        {
          "id": "env-001",
          "name": "分页查询环境列表",
          "method": "GET",
          "path": "/v1.0/system/environment/environments/page",
          "params": [
            "pageNum",
            "pageSize",
            "envCode",
            "envName",
            "status"
          ],
          "response": "PageInfo<DevEnvironmentVo>"
        },
        {
          "id": "env-002",
          "name": "查询环境列表",
          "method": "GET",
          "path": "/v1.0/system/environment/environments/list",
          "params": [],
          "response": "List<DevEnvironmentVo>"
        },
        {
          "id": "env-003",
          "name": "根据 ID 查询环境",
          "method": "GET",
          "path": "/v1.0/system/environment/environments/{id}",
          "params": [
            "id"
          ],
          "response": "DevEnvironmentVo"
        },
        {
          "id": "env-004",
          "name": "根据编码查询环境",
          "method": "GET",
          "path": "/v1.0/system/environment/environments/code/{envCode}",
          "params": [
            "envCode"
          ],
          "response": "DevEnvironmentVo"
        },
        {
          "id": "env-005",
          "name": "新增环境",
          "method": "POST",
          "path": "/v1.0/system/environment/environments",
          "params": [
            "envCode",
            "envName",
            "description",
            "sort",
            "status"
          ],
          "response": "void"
        },
        {
          "id": "env-006",
          "name": "修改环境",
          "method": "POST",
          "path": "/v1.0/system/environment/environments/update",
          "params": [
            "id",
            "envCode",
            "envName",
            "description",
            "sort",
            "status"
          ],
          "response": "void"
        },
        {
          "id": "env-007",
          "name": "删除环境",
          "method": "DELETE",
          "path": "/v1.0/system/environment/environments/{id}",
          "params": [
            "id"
          ],
          "response": "void"
        }
      ]
    },
    {
      "module": "产品管理",
      "moduleCode": "product",
      "controller": "DevProductController",
      "endpoints": [
        {
          "id": "product-001",
          "name": "分页查询产品列表",
          "method": "GET",
          "path": "/v1.0/system/product/products/page",
          "params": [
            "pageNum",
            "pageSize",
            "productName",
            "productCode",
            "status",
            "category",
            "manager",
            "envCode"
          ],
          "response": "PageInfo<DevProductVo>"
        },
        {
          "id": "product-002",
          "name": "查询产品列表",
          "method": "GET",
          "path": "/v1.0/system/product/products/list",
          "params": [],
          "response": "List<DevProductVo>"
        },
        {
          "id": "product-003",
          "name": "根据 ID 查询产品",
          "method": "GET",
          "path": "/v1.0/system/product/products/{id}",
          "params": [
            "id"
          ],
          "response": "DevProductVo"
        },
        {
          "id": "product-004",
          "name": "新增产品",
          "method": "POST",
          "path": "/v1.0/system/product/products",
          "params": [
            "productName",
            "productCode",
            "description",
            "status",
            "category",
            "version",
            "manager",
            "envCode",
            "accessUrl",
            "accessAccount",
            "accessPassword",
            "sort"
          ],
          "response": "void"
        },
        {
          "id": "product-005",
          "name": "修改产品",
          "method": "POST",
          "path": "/v1.0/system/product/products/update",
          "params": [
            "id",
            "productName",
            "productCode",
            "description",
            "status",
            "category",
            "version",
            "manager",
            "envCode",
            "accessUrl",
            "accessAccount",
            "accessPassword",
            "sort"
          ],
          "response": "void"
        },
        {
          "id": "product-006",
          "name": "删除产品",
          "method": "DELETE",
          "path": "/v1.0/system/product/products/{id}",
          "params": [
            "id"
          ],
          "response": "void"
        }
      ]
    },
    {
      "module": "项目管理",
      "moduleCode": "project",
      "controller": "DevProjectController",
      "endpoints": [
        {
          "id": "project-001",
          "name": "分页查询项目列表",
          "method": "GET",
          "path": "/v1.0/system/project/projects/page",
          "params": [
            "pageNum",
            "pageSize",
            "projectName",
            "projectCode",
            "status",
            "manager"
          ],
          "response": "PageInfo<DevProjectVo>"
        },
        {
          "id": "project-002",
          "name": "查询项目列表",
          "method": "GET",
          "path": "/v1.0/system/project/projects/list",
          "params": [],
          "response": "List<DevProjectVo>"
        },
        {
          "id": "project-003",
          "name": "根据 ID 查询项目",
          "method": "GET",
          "path": "/v1.0/system/project/projects/{id}",
          "params": [
            "id"
          ],
          "response": "DevProjectVo"
        },
        {
          "id": "project-004",
          "name": "新增项目",
          "method": "POST",
          "path": "/v1.0/system/project/projects",
          "params": [
            "projectName",
            "projectCode",
            "description",
            "status",
            "startDate",
            "endDate",
            "manager",
            "sort"
          ],
          "response": "void"
        },
        {
          "id": "project-005",
          "name": "修改项目",
          "method": "POST",
          "path": "/v1.0/system/project/projects/update",
          "params": [
            "id",
            "projectName",
            "projectCode",
            "description",
            "status",
            "startDate",
            "endDate",
            "manager",
            "sort"
          ],
          "response": "void"
        },
        {
          "id": "project-006",
          "name": "删除项目",
          "method": "DELETE",
          "path": "/v1.0/system/project/projects/{id}",
          "params": [
            "id"
          ],
          "response": "void"
        }
      ]
    },
    {
      "module": "菜单管理",
      "moduleCode": "menu",
      "controller": "SysMenuController",
      "endpoints": [
        {
          "id": "menu-001",
          "name": "分页查询菜单列表",
          "method": "GET",
          "path": "/v1.0/system/menu/menus/page",
          "params": [
            "pageNum",
            "pageSize",
            "menuName",
            "status"
          ],
          "response": "PageInfo<SysMenuVo>"
        },
        {
          "id": "menu-002",
          "name": "查询菜单树",
          "method": "GET",
          "path": "/v1.0/system/menu/menus/tree",
          "params": [],
          "response": "List<SysMenuVo>"
        },
        {
          "id": "menu-003",
          "name": "根据 ID 查询菜单",
          "method": "GET",
          "path": "/v1.0/system/menu/menus/{id}",
          "params": [
            "id"
          ],
          "response": "SysMenuVo"
        },
        {
          "id": "menu-004",
          "name": "查询子菜单列表",
          "method": "GET",
          "path": "/v1.0/system/menu/menus/children/{parentId}",
          "params": [
            "parentId"
          ],
          "response": "List<SysMenuVo>"
        },
        {
          "id": "menu-005",
          "name": "新增菜单",
          "method": "POST",
          "path": "/v1.0/system/menu/menus",
          "params": [
            "parentId",
            "menuName",
            "menuCode",
            "menuType",
            "path",
            "component",
            "icon",
            "sort",
            "status",
            "permission"
          ],
          "response": "void"
        },
        {
          "id": "menu-006",
          "name": "修改菜单",
          "method": "POST",
          "path": "/v1.0/system/menu/menus/update",
          "params": [
            "id",
            "parentId",
            "menuName",
            "menuCode",
            "menuType",
            "path",
            "component",
            "icon",
            "sort",
            "status",
            "permission"
          ],
          "response": "void"
        },
        {
          "id": "menu-007",
          "name": "删除菜单",
          "method": "DELETE",
          "path": "/v1.0/system/menu/menus/{id}",
          "params": [
            "id"
          ],
          "response": "void"
        }
      ]
    },
    {
      "module": "角色管理",
      "moduleCode": "role",
      "controller": "SysRoleController",
      "endpoints": [
        {
          "id": "role-001",
          "name": "分页查询角色列表",
          "method": "GET",
          "path": "/v1.0/system/role/roles/page",
          "params": [
            "pageNum",
            "pageSize",
            "roleName",
            "status"
          ],
          "response": "PageInfo<SysRoleVo>"
        },
        {
          "id": "role-002",
          "name": "查询角色列表",
          "method": "GET",
          "path": "/v1.0/system/role/roles/list",
          "params": [],
          "response": "List<SysRoleVo>"
        },
        {
          "id": "role-003",
          "name": "根据 ID 查询角色",
          "method": "GET",
          "path": "/v1.0/system/role/roles/{id}",
          "params": [
            "id"
          ],
          "response": "SysRoleVo"
        },
        {
          "id": "role-004",
          "name": "新增角色",
          "method": "POST",
          "path": "/v1.0/system/role/roles",
          "params": [
            "roleName",
            "roleCode",
            "description",
            "status",
            "sort"
          ],
          "response": "void"
        },
        {
          "id": "role-005",
          "name": "修改角色",
          "method": "POST",
          "path": "/v1.0/system/role/roles/update",
          "params": [
            "id",
            "roleName",
            "roleCode",
            "description",
            "status",
            "sort"
          ],
          "response": "void"
        },
        {
          "id": "role-006",
          "name": "删除角色",
          "method": "DELETE",
          "path": "/v1.0/system/role/roles/{id}",
          "params": [
            "id"
          ],
          "response": "void"
        }
      ]
    },
    {
      "module": "用户管理",
      "moduleCode": "user",
      "controller": "SysUserController",
      "endpoints": [
        {
          "id": "user-001",
          "name": "分页查询用户列表",
          "method": "GET",
          "path": "/v1.0/system/user/users/page",
          "params": [
            "pageNum",
            "pageSize",
            "username",
            "nickname",
            "status"
          ],
          "response": "PageInfo<SysUserVo>"
        },
        {
          "id": "user-002",
          "name": "根据 ID 查询用户",
          "method": "GET",
          "path": "/v1.0/system/user/users/{id}",
          "params": [
            "id"
          ],
          "response": "SysUserVo"
        },
        {
          "id": "user-003",
          "name": "新增用户",
          "method": "POST",
          "path": "/v1.0/system/user/users",
          "params": [
            "username",
            "password",
            "nickname",
            "email",
            "phone",
            "avatar",
            "status",
            "deptId"
          ],
          "response": "void"
        },
        {
          "id": "user-004",
          "name": "修改用户",
          "method": "POST",
          "path": "/v1.0/system/user/users/update",
          "params": [
            "id",
            "username",
            "password",
            "nickname",
            "email",
            "phone",
            "avatar",
            "status",
            "deptId"
          ],
          "response": "void"
        },
        {
          "id": "user-005",
          "name": "删除用户",
          "method": "DELETE",
          "path": "/v1.0/system/user/users/{id}",
          "params": [
            "id"
          ],
          "response": "void"
        }
      ]
    },
    {
      "module": "用户角色管理",
      "moduleCode": "user-role",
      "controller": "SysUserRoleController",
      "endpoints": [
        {
          "id": "userrole-001",
          "name": "获取用户角色信息",
          "method": "GET",
          "path": "/v1.0/system/user-role/users/{userId}/roles",
          "params": [
            "userId"
          ],
          "response": "SysUserRoleVo"
        },
        {
          "id": "userrole-002",
          "name": "获取用户角色 ID 列表",
          "method": "GET",
          "path": "/v1.0/system/user-role/users/{userId}/role-ids",
          "params": [
            "userId"
          ],
          "response": "List<Long>"
        },
        {
          "id": "userrole-003",
          "name": "分配用户角色",
          "method": "POST",
          "path": "/v1.0/system/user-role/users/{userId}/roles/assign",
          "params": [
            "userId",
            "roleIds"
          ],
          "response": "void"
        },
        {
          "id": "userrole-004",
          "name": "移除用户角色",
          "method": "DELETE",
          "path": "/v1.0/system/user-role/users/{userId}/roles/{roleId}",
          "params": [
            "userId",
            "roleId"
          ],
          "response": "void"
        },
        {
          "id": "userrole-005",
          "name": "清空用户角色",
          "method": "DELETE",
          "path": "/v1.0/system/user-role/users/{userId}/roles",
          "params": [
            "userId"
          ],
          "response": "void"
        }
      ]
    }
  ],
  "versionIds": [
    "v0.0.2",
    "v0.0.3",
    "v0.0.4",
    "v0.0.5",
    "v0.0.6",
    "v0.0.7",
    "v0.0.8",
    "v0.0.9"
  ],
  "url": "http://jffe.techgp.cn/小程序转发作品数据统计_20260331180000",
  "message": "后端规格已同步 8 条至项目 小程序转发作品数据统计_20260331180000"
}
```

---
