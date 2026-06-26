export const databaseTools = [
  { name: "list_databases", description: "List databases", inputSchema: { type: "object", properties: { type: { type: "string", enum: ["mysql", "postgresql", "redis"] } }, required: ["type"] } },
  { name: "create_database", description: "Create database", inputSchema: { type: "object", properties: { type: { type: "string" }, db: { type: "object" } }, required: ["type", "db"] } },
  { name: "delete_database", description: "Delete database", inputSchema: { type: "object", properties: { type: { type: "string" }, id: { type: "number" } }, required: ["type", "id"] } },
  { name: "get_database", description: "Get database details", inputSchema: { type: "object", properties: { type: { type: "string" }, id: { type: "number" } }, required: ["type", "id"] } },
  { name: "mysql_bind_user", description: "MySQL: Bind/create user", inputSchema: { type: "object", properties: { database: { type: "string" }, db: { type: "string" }, username: { type: "string" }, password: { type: "string" }, permission: { type: "string" } }, required: ["database", "db", "username", "password", "permission"] } },
  { name: "mysql_change_password", description: "MySQL: Change user password", inputSchema: { type: "object", properties: { id: { type: "number" }, database: { type: "string" }, from: { type: "string" }, type: { type: "string" }, value: { type: "string" } }, required: ["id", "database", "from", "type", "value"] } },
  { name: "mysql_change_access", description: "MySQL: Change remote access", inputSchema: { type: "object", properties: { id: { type: "number" }, database: { type: "string" }, from: { type: "string" }, type: { type: "string" }, value: { type: "string" } }, required: ["id", "database", "from", "type", "value"] } },
  { name: "mysql_get_info", description: "MySQL: Get server info", inputSchema: { type: "object", properties: { from: { type: "string" } } } },
  { name: "mysql_get_remote_access", description: "MySQL: Get remote access config", inputSchema: { type: "object", properties: {} } },
  { name: "mysql_update_remote_access", description: "MySQL: Update remote access", inputSchema: { type: "object", properties: { privilege: { type: "boolean" } }, required: ["privilege"] } },
  { name: "mysql_get_status", description: "MySQL: Get server status", inputSchema: { type: "object", properties: {} } },
  { name: "mysql_get_variables", description: "MySQL: Get variables", inputSchema: { type: "object", properties: {} } },
  { name: "mysql_update_variables", description: "MySQL: Update variables", inputSchema: { type: "object", properties: { variables: { type: "object" } }, required: ["variables"] } },
  { name: "postgresql_bind_user", description: "PostgreSQL: Bind/create user", inputSchema: { type: "object", properties: { database: { type: "string" }, name: { type: "string" }, username: { type: "string" }, password: { type: "string" }, superUser: { type: "boolean" } }, required: ["database", "name", "username", "password"] } },
  { name: "postgresql_change_password", description: "PostgreSQL: Change password", inputSchema: { type: "object", properties: { id: { type: "number" }, database: { type: "string" }, from: { type: "string" }, type: { type: "string" }, value: { type: "string" } }, required: ["id", "database", "from", "type", "value"] } },
  { name: "postgresql_change_privileges", description: "PostgreSQL: Change privileges", inputSchema: { type: "object", properties: { id: { type: "number" }, database: { type: "string" }, from: { type: "string" }, type: { type: "string" }, value: { type: "string" } }, required: ["id", "database", "from", "type", "value"] } },
  { name: "postgresql_list_databases", description: "PostgreSQL: List databases", inputSchema: { type: "object", properties: {} } },
  { name: "redis_get_conf", description: "Redis: Get configuration", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "redis_update_conf", description: "Redis: Update configuration", inputSchema: { type: "object", properties: { id: { type: "number" }, content: { type: "string" } }, required: ["id"] } },
  { name: "redis_change_password", description: "Redis: Change password", inputSchema: { type: "object", properties: { id: { type: "number" }, value: { type: "string" } }, required: ["id", "value"] } },
  { name: "redis_get_status", description: "Redis: Get status", inputSchema: { type: "object", properties: {} } },
  { name: "redis_get_persistence_conf", description: "Redis: Get persistence config", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "redis_update_persistence_conf", description: "Redis: Update persistence", inputSchema: { type: "object", properties: { id: { type: "number" }, appendonly: { type: "string" }, appendfsync: { type: "string" }, save: { type: "string" } }, required: ["id"] } },
];

export async function handleDatabaseTool(client: any, name: string, args: any) {
  switch (name) {
    case "list_databases": return await client.listDatabases(args?.type);
    case "create_database": return await client.createDatabase(args?.type, args?.db);
    case "delete_database": return await client.deleteDatabase(args?.type, args?.id);
    case "get_database": return await client.getDatabase(args?.type, args?.id);
    case "mysql_bind_user": return await client.mysqlBindUser(args);
    case "mysql_change_password": return await client.mysqlChangePassword(args);
    case "mysql_change_access": return await client.mysqlChangeAccess(args);
    case "mysql_get_info": return await client.mysqlGetInfo(args?.from);
    case "mysql_get_remote_access": return await client.mysqlGetRemoteAccess();
    case "mysql_update_remote_access": return await client.mysqlUpdateRemoteAccess(args?.privilege);
    case "mysql_get_status": return await client.mysqlGetStatus();
    case "mysql_get_variables": return await client.mysqlGetVariables();
    case "mysql_update_variables": return await client.mysqlUpdateVariables(args?.variables);
    case "postgresql_bind_user": return await client.postgresqlBindUser(args);
    case "postgresql_change_password": return await client.postgresqlChangePassword(args);
    case "postgresql_change_privileges": return await client.postgresqlChangePrivileges(args);
    case "postgresql_list_databases": return await client.postgresqlListDatabases();
    case "redis_get_conf": return await client.redisGetConf(args?.id);
    case "redis_update_conf": return await client.redisUpdateConf(args);
    case "redis_change_password": return await client.redisChangePassword(args);
    case "redis_get_status": return await client.redisGetStatus();
    case "redis_get_persistence_conf": return await client.redisGetPersistenceConf(args?.id);
    case "redis_update_persistence_conf": return await client.redisUpdatePersistenceConf(args?.id, args);
    default: return null;
  }
}
