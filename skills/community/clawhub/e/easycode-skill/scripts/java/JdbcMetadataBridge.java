import com.fasterxml.jackson.databind.ObjectMapper;

import java.sql.*;
import java.util.*;

public class JdbcMetadataBridge {
    private static final ObjectMapper MAPPER = new ObjectMapper();

    public static void main(String[] args) throws Exception {
        Map<String, String> a = parseArgs(args);
        String dbType = req(a, "db-type");
        String url = req(a, "url");
        String user = req(a, "user");
        String pass = req(a, "pass");
        String tablesRaw = req(a, "tables");
        String driverClass = a.getOrDefault("driver-class", defaultDriverClass(dbType));
        String numberType = a.getOrDefault("number-type", "Long");
        String timeType = a.getOrDefault("time-type", "Date");

        if (driverClass != null && !driverClass.isBlank()) {
            Class.forName(driverClass);
        }

        List<String> tables = new ArrayList<>();
        for (String t : tablesRaw.split(",")) {
            if (!t.isBlank()) {
                tables.add(t.trim());
            }
        }

        Map<String, List<Map<String, Object>>> result = new LinkedHashMap<>();
        Map<String, String> tableComments = new LinkedHashMap<>();
        try (Connection conn = DriverManager.getConnection(url, user, pass)) {
            DatabaseMetaData meta = conn.getMetaData();
            String schema = detectSchema(conn, dbType, user);
            for (String table : tables) {
                String[] ref = normalizeQualifiedTable(schema, table);
                result.put(table, loadColumns(conn, meta, ref[0], ref[1], numberType, timeType));
                tableComments.put(table, loadTableComment(conn, meta, ref[0], ref[1]));
            }
        }

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("tables", result);
        out.put("table_comments", tableComments);
        System.out.println(MAPPER.writeValueAsString(out));
    }

    private static String detectSchema(Connection conn, String dbType, String user) {
        try {
            String s = conn.getSchema();
            if (s != null && !s.isBlank()) {
                return s;
            }
        } catch (SQLException ignored) {
        }

        if ("postgresql".equalsIgnoreCase(dbType)) {
            return "public";
        }
        if ("oracle".equalsIgnoreCase(dbType)) {
            return user == null ? null : user.toUpperCase(Locale.ROOT);
        }
        return null;
    }

    private static List<Map<String, Object>> loadColumns(Connection conn, DatabaseMetaData meta, String schema, String table, String numberType, String timeType) throws SQLException {
        String effectiveSchema = schema;
        String effectiveTable = table;
        if (effectiveSchema != null && !effectiveSchema.isBlank()) {
            effectiveSchema = effectiveSchema.toUpperCase(Locale.ROOT);
        }
        if (effectiveTable != null && !effectiveTable.isBlank()) {
            effectiveTable = effectiveTable.toUpperCase(Locale.ROOT);
        }

        Map<String, String> commentByColumn = loadOracleColumnComments(conn, effectiveSchema, effectiveTable);

        Set<String> pks = new HashSet<>();
        try (ResultSet rs = meta.getPrimaryKeys(null, effectiveSchema, effectiveTable)) {
            while (rs.next()) {
                String col = rs.getString("COLUMN_NAME");
                if (col != null) {
                    pks.add(col.toLowerCase(Locale.ROOT));
                }
            }
        }

        List<Map<String, Object>> cols = new ArrayList<>();
        try (ResultSet rs = meta.getColumns(null, effectiveSchema, effectiveTable, "%")) {
            while (rs.next()) {
                String colName = nvl(rs.getString("COLUMN_NAME"));
                int dataType = rs.getInt("DATA_TYPE");
                int scale = rs.getInt("DECIMAL_DIGITS");
                String typeName = nvl(rs.getString("TYPE_NAME"));
                String comment = nvl(rs.getString("REMARKS"));
                if (comment.isBlank()) {
                    comment = nvl(commentByColumn.get(colName.toUpperCase(Locale.ROOT)));
                }
                String javaType = javaTypeOf(dataType, scale, numberType, timeType);

                Map<String, Object> c = new LinkedHashMap<>();
                c.put("name", colName);
                c.put("comment", comment);
                c.put("type", javaType);
                c.put("short_type", shortTypeOf(javaType));
                c.put("sql_type", typeName);
                c.put("is_pk", pks.contains(colName.toLowerCase(Locale.ROOT)));
                cols.add(c);
            }
        }

        return cols;
    }

    private static String loadTableComment(Connection conn, DatabaseMetaData meta, String schema, String table) {
        String comment = "";
        try (ResultSet rs = meta.getTables(null, schema, table, new String[]{"TABLE"})) {
            if (rs.next()) {
                comment = nvl(rs.getString("REMARKS"));
            }
        } catch (Exception ignored) {
        }
        if (!comment.isBlank()) {
            return comment;
        }
        if (schema == null || schema.isBlank() || table == null || table.isBlank()) {
            return "";
        }
        String sql = "SELECT COMMENTS FROM ALL_TAB_COMMENTS WHERE OWNER = ? AND TABLE_NAME = ?";
        try (PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, schema.toUpperCase(Locale.ROOT));
            ps.setString(2, table.toUpperCase(Locale.ROOT));
            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    return nvl(rs.getString("COMMENTS"));
                }
            }
        } catch (Exception ignored) {
        }
        return "";
    }

    private static String[] normalizeQualifiedTable(String defaultSchema, String rawTable) {
        String schema = defaultSchema;
        String table = rawTable;
        if (rawTable != null && rawTable.contains(".")) {
            String[] parts = rawTable.split("\\.", 2);
            if (parts.length == 2) {
                schema = parts[0];
                table = parts[1];
            }
        }
        if (schema == null) {
            schema = "";
        }
        if (table == null) {
            table = "";
        }
        return new String[]{schema.toUpperCase(Locale.ROOT), table.toUpperCase(Locale.ROOT)};
    }

    private static Map<String, String> loadOracleColumnComments(Connection conn, String schema, String table) {
        Map<String, String> map = new HashMap<>();
        if (schema == null || schema.isBlank() || table == null || table.isBlank()) {
            return map;
        }
        String sql = "SELECT COLUMN_NAME, COMMENTS FROM ALL_COL_COMMENTS WHERE OWNER = ? AND TABLE_NAME = ?";
        try (PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, schema.toUpperCase(Locale.ROOT));
            ps.setString(2, table.toUpperCase(Locale.ROOT));
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    String col = rs.getString("COLUMN_NAME");
                    String comment = rs.getString("COMMENTS");
                    if (col != null) {
                        map.put(col.toUpperCase(Locale.ROOT), nvl(comment));
                    }
                }
            }
        } catch (Exception ignored) {
            // Best-effort fallback only; metadata REMARKS still works for other DBs.
        }
        return map;
    }

    private static String javaTypeOf(int jdbcType, int scale, String numberType, String timeType) {
        String numberPref = numberType == null ? "Long" : numberType.trim();
        String timePref = timeType == null ? "Date" : timeType.trim();
        switch (jdbcType) {
            case Types.BIT:
            case Types.BOOLEAN:
                return "java.lang.Boolean";
            case Types.TINYINT:
                return "java.lang.Byte";
            case Types.SMALLINT:
                return "java.lang.Short";
            case Types.INTEGER:
                return "java.lang.Integer";
            case Types.BIGINT:
                return "java.lang.Long";
            case Types.FLOAT:
            case Types.REAL:
                return "java.lang.Float";
            case Types.DOUBLE:
                return "java.lang.Double";
            case Types.NUMERIC:
            case Types.DECIMAL:
                if ("BigDecimal".equalsIgnoreCase(numberPref)) {
                    return "java.math.BigDecimal";
                }
                if (scale > 0) {
                    return "java.math.BigDecimal";
                }
                return "java.lang.Long";
            case Types.DATE:
            case Types.TIME:
            case Types.TIMESTAMP:
            case Types.TIMESTAMP_WITH_TIMEZONE:
                if ("LocalDateTime".equalsIgnoreCase(timePref)) {
                    if (jdbcType == Types.DATE) {
                        return "java.time.LocalDate";
                    }
                    if (jdbcType == Types.TIME) {
                        return "java.time.LocalTime";
                    }
                    return "java.time.LocalDateTime";
                }
                return "java.util.Date";
            case Types.CHAR:
            case Types.VARCHAR:
            case Types.LONGVARCHAR:
            case Types.NCHAR:
            case Types.NVARCHAR:
            case Types.LONGNVARCHAR:
                return "java.lang.String";
            case Types.BINARY:
            case Types.VARBINARY:
            case Types.LONGVARBINARY:
            case Types.BLOB:
                return "byte[]";
            case Types.CLOB:
            case Types.NCLOB:
                return "java.lang.String";
            default:
                return "java.lang.String";
        }
    }

    private static String shortTypeOf(String type) {
        if (type == null || type.isBlank()) {
            return "Object";
        }
        if ("byte[]".equals(type)) {
            return "byte[]";
        }
        int idx = type.lastIndexOf('.');
        return idx >= 0 ? type.substring(idx + 1) : type;
    }

    private static String defaultDriverClass(String dbType) {
        if (dbType == null) return "";
        switch (dbType.toLowerCase(Locale.ROOT)) {
            case "mysql":
                return "com.mysql.cj.jdbc.Driver";
            case "postgresql":
                return "org.postgresql.Driver";
            case "oracle":
                return "oracle.jdbc.OracleDriver";
            case "sqlserver":
                return "com.microsoft.sqlserver.jdbc.SQLServerDriver";
            default:
                return "";
        }
    }

    private static String nvl(String s) {
        return s == null ? "" : s;
    }

    private static Map<String, String> parseArgs(String[] args) {
        Map<String, String> map = new HashMap<>();
        for (int i = 0; i < args.length; i++) {
            String s = args[i];
            if (!s.startsWith("--")) continue;
            String k = s.substring(2);
            String v = i + 1 < args.length ? args[++i] : "";
            map.put(k, v);
        }
        return map;
    }

    private static String req(Map<String, String> map, String k) {
        String v = map.get(k);
        if (v == null || v.isBlank()) {
            throw new IllegalArgumentException("Missing --" + k);
        }
        return v;
    }
}
