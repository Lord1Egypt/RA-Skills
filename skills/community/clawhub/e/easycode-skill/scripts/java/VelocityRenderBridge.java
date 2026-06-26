import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.velocity.VelocityContext;
import org.apache.velocity.app.VelocityEngine;
import org.apache.velocity.runtime.RuntimeConstants;

import java.io.IOException;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.lang.reflect.Field;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.regex.Pattern;

public class VelocityRenderBridge {
    private static final ObjectMapper MAPPER = new ObjectMapper();

    private static final Pattern RE_GLOBAL_1 = Pattern.compile("\\$!?%s(\\\\W)");

    public static void main(String[] args) throws Exception {
        Map<String, String> argMap = parseArgs(args);
        String template = Files.readString(Path.of(requireArg(argMap, "template-file")), StandardCharsets.UTF_8);
        Map<String, Object> payload = readJson(requireArg(argMap, "context-file"));

        TableInfo tableInfo = toTableInfo(payload.get("tableInfo"));
        String author = String.valueOf(payload.getOrDefault("author", "unknown"));

        @SuppressWarnings("unchecked")
        Map<String, String> globalMacros = (Map<String, String>) payload.getOrDefault("globalMacros", Collections.emptyMap());

        String mergedTemplate = addGlobalConfig(template + "\n", globalMacros);

        Callback callback = new Callback();
        callback.setSavePath(tableInfo.getSavePath());
        callback.setFileName(tableInfo.getName() + ".java");

        Set<String> importList = new LinkedHashSet<>();
        if (tableInfo.getFullColumn() != null) {
            for (ColumnInfo column : tableInfo.getFullColumn()) {
                if (column.getType() != null && !column.getType().startsWith("java.lang.")) {
                    importList.add(column.getType());
                }
            }
        }

        VelocityEngine engine = new VelocityEngine();
        engine.setProperty(RuntimeConstants.RUNTIME_LOG_LOGSYSTEM_CLASS, "org.apache.velocity.runtime.log.NullLogSystem");
        VelocityContext context = new VelocityContext();
        context.put("tableInfo", tableInfo);
        context.put("author", author);
        context.put("tool", new Tool());
        context.put("time", new TimeTool());
        context.put("callback", callback);
        context.put("importList", importList);

        String rendered = evaluate(engine, context, mergedTemplate);

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("rendered", ltrim(rendered));
        out.put("savePath", callback.getSavePath());
        out.put("fileName", callback.getFileName());
        System.out.println(MAPPER.writeValueAsString(out));
    }

    private static String evaluate(VelocityEngine engine, VelocityContext context, String template) {
        StringWriter writer = new StringWriter();
        try {
            engine.evaluate(context, writer, "easycode-skill", template);
        } catch (Exception e) {
            StringWriter sw = new StringWriter();
            e.printStackTrace(new PrintWriter(sw));
            return "在生成代码时，模板发生了如下语法错误：\n" + sw.toString().replace("\r", "");
        }
        return writer.toString();
    }

    private static String addGlobalConfig(String template, Map<String, String> globalConfigs) {
        String out = template;
        for (Map.Entry<String, String> entry : globalConfigs.entrySet()) {
            String name = entry.getKey();
            String value = entry.getValue();
            if (value == null) {
                value = "";
            }
            value = value.replace("\\", "\\\\").replace("$", "\\$");
            out = out.replaceAll("\\$!?" + Pattern.quote(name) + "(\\W)", "\\$!{" + name + "}$1");
            out = out.replaceAll("\\$!?\\{" + Pattern.quote(name) + "}", value);
        }
        return out;
    }

    private static String ltrim(String s) {
        int idx = 0;
        while (idx < s.length() && Character.isWhitespace(s.charAt(idx))) {
            idx++;
        }
        return s.substring(idx);
    }

    private static Map<String, Object> readJson(String file) throws IOException {
        return MAPPER.readValue(Path.of(file).toFile(), new TypeReference<Map<String, Object>>() {});
    }

    @SuppressWarnings("unchecked")
    private static TableInfo toTableInfo(Object obj) {
        Map<String, Object> map = obj instanceof Map ? (Map<String, Object>) obj : Collections.emptyMap();
        TableInfo t = new TableInfo();
        t.setName(str(map.get("name")));
        t.setPreName(str(map.get("preName")));
        t.setComment(str(map.get("comment")));
        t.setTemplateGroupName(str(map.get("templateGroupName")));
        t.setSavePackageName(str(map.get("savePackageName")));
        t.setSavePath(str(map.get("savePath")));
        t.setSaveModelName(str(map.get("saveModelName")));

        t.setObj(toObj(map.get("obj")));
        t.setFullColumn(toColumns(map.get("fullColumn")));
        t.setPkColumn(toColumns(map.get("pkColumn")));
        t.setOtherColumn(toColumns(map.get("otherColumn")));
        return t;
    }

    @SuppressWarnings("unchecked")
    private static ObjInfo toObj(Object obj) {
        Map<String, Object> map = obj instanceof Map ? (Map<String, Object>) obj : Collections.emptyMap();
        ObjInfo o = new ObjInfo();
        o.setName(str(map.get("name")));
        Object parentObj = map.get("parent");
        if (parentObj instanceof Map) {
            ObjInfo parent = new ObjInfo();
            parent.setName(str(((Map<String, Object>) parentObj).get("name")));
            o.setParent(parent);
        }
        DataTypeInfo dt = new DataTypeInfo();
        Object dtObj = map.get("dataType");
        if (dtObj instanceof Map) {
            dt.setTypeName(str(((Map<String, Object>) dtObj).get("typeName")));
        }
        o.setDataType(dt);
        return o;
    }

    @SuppressWarnings("unchecked")
    private static List<ColumnInfo> toColumns(Object obj) {
        if (!(obj instanceof List)) {
            return new ArrayList<>();
        }
        List<ColumnInfo> cols = new ArrayList<>();
        for (Object item : (List<Object>) obj) {
            if (!(item instanceof Map)) {
                continue;
            }
            Map<String, Object> map = (Map<String, Object>) item;
            ColumnInfo c = new ColumnInfo();
            c.setName(str(map.get("name")));
            c.setComment(str(map.get("comment")));
            c.setType(str(map.get("type")));
            c.setShortType(str(map.get("shortType")));
            Object ext = map.get("ext");
            if (ext instanceof Map) {
                c.setExt((Map<String, Object>) ext);
            } else {
                c.setExt(new LinkedHashMap<>());
            }
            c.setObj(toObj(map.get("obj")));
            cols.add(c);
        }
        return cols;
    }

    private static String str(Object o) {
        return o == null ? "" : String.valueOf(o);
    }

    private static Map<String, String> parseArgs(String[] args) {
        Map<String, String> map = new HashMap<>();
        for (int i = 0; i < args.length; i++) {
            String s = args[i];
            if (!s.startsWith("--")) {
                continue;
            }
            String key = s.substring(2);
            String val = i + 1 < args.length ? args[++i] : "";
            map.put(key, val);
        }
        return map;
    }

    private static String requireArg(Map<String, String> args, String key) {
        String val = args.get(key);
        if (val == null || val.isBlank()) {
            throw new IllegalArgumentException("Missing required --" + key);
        }
        return val;
    }

    public static class Callback {
        private String savePath;
        private String fileName;

        public String getSavePath() {
            return savePath;
        }

        public void setSavePath(String savePath) {
            this.savePath = savePath;
        }

        public String getFileName() {
            return fileName;
        }

        public void setFileName(String fileName) {
            this.fileName = fileName;
        }
    }

    public static class TimeTool {
        public String currTime() {
            return currTime("yyyy-MM-dd HH:mm:ss");
        }

        public String currTime(String pattern) {
            return LocalDateTime.now().format(DateTimeFormatter.ofPattern(pattern));
        }
    }

    public static class Tool {
        public String append(Object... objects) {
            if (objects == null || objects.length == 0) {
                return "";
            }
            StringBuilder b = new StringBuilder();
            for (Object obj : objects) {
                if (obj != null) {
                    b.append(obj);
                }
            }
            return b.toString();
        }

        public String firstLowerCase(String name) {
            if (name == null || name.isEmpty()) return name;
            return Character.toLowerCase(name.charAt(0)) + name.substring(1);
        }

        public String firstUpperCase(String name) {
            if (name == null || name.isEmpty()) return name;
            return Character.toUpperCase(name.charAt(0)) + name.substring(1);
        }

        public String getClassName(String name) {
            return firstUpperCase(getJavaName(name));
        }

        public String getJavaName(String name) {
            if (name == null) return "";
            String n = name.toLowerCase(Locale.ROOT);
            StringBuilder out = new StringBuilder();
            boolean up = false;
            for (char ch : n.toCharArray()) {
                if (ch == '_' || ch == '-') {
                    up = true;
                    continue;
                }
                if (up) {
                    out.append(Character.toUpperCase(ch));
                    up = false;
                } else {
                    out.append(ch);
                }
            }
            return out.toString();
        }

        public String getClsNameByFullName(String fullName) {
            if (fullName == null || fullName.isEmpty()) return fullName;
            int genericIdx = fullName.indexOf('<');
            if (genericIdx == -1) {
                int idx = fullName.lastIndexOf('.');
                return idx >= 0 ? fullName.substring(idx + 1) : fullName;
            }
            String className = fullName.substring(0, genericIdx);
            int idx = className.lastIndexOf('.');
            return idx >= 0 ? className.substring(idx + 1) : className;
        }

        public String getClsFullNameRemoveGeneric(String fullName) {
            if (fullName == null) return null;
            int idx = fullName.indexOf('<');
            return idx == -1 ? fullName : fullName.substring(0, idx);
        }

        public Set<Object> newHashSet(Object... items) {
            LinkedHashSet<Object> set = new LinkedHashSet<>();
            if (items != null) {
                Collections.addAll(set, items);
            }
            return set;
        }

        public List<Object> newArrayList(Object... items) {
            ArrayList<Object> list = new ArrayList<>();
            if (items != null) {
                Collections.addAll(list, items);
            }
            return list;
        }

        public Map<Object, Object> newLinkedHashMap() {
            return new LinkedHashMap<>();
        }

        public Map<Object, Object> newHashMap() {
            return new HashMap<>();
        }

        public void call(Object... obj) {
        }

        public Object getField(Object obj, String fieldName) {
            if (obj == null || fieldName == null || fieldName.isEmpty()) {
                return null;
            }
            Class<?> cls = obj.getClass();
            while (cls != null && cls != Object.class) {
                try {
                    Field f = cls.getDeclaredField(fieldName);
                    f.setAccessible(true);
                    return f.get(obj);
                } catch (NoSuchFieldException ignored) {
                    cls = cls.getSuperclass();
                } catch (IllegalAccessException e) {
                    return null;
                }
            }
            return null;
        }

        public String serial() {
            Random random = new Random();
            StringBuilder builder = new StringBuilder();
            if (random.nextFloat() > 0.5F) {
                builder.append("-");
            }
            builder.append(random.nextInt(9) + 1);
            while (builder.length() < 18) {
                builder.append(random.nextInt(10));
            }
            builder.append("L");
            return builder.toString();
        }
    }

    public static class TableInfo {
        private ObjInfo obj = new ObjInfo();
        private String name;
        private String preName;
        private String comment;
        private String templateGroupName;
        private List<ColumnInfo> fullColumn = new ArrayList<>();
        private List<ColumnInfo> pkColumn = new ArrayList<>();
        private List<ColumnInfo> otherColumn = new ArrayList<>();
        private String savePackageName;
        private String savePath;
        private String saveModelName;

        public ObjInfo getObj() { return obj; }
        public void setObj(ObjInfo obj) { this.obj = obj; }
        public String getName() { return name; }
        public void setName(String name) { this.name = name; }
        public String getPreName() { return preName; }
        public void setPreName(String preName) { this.preName = preName; }
        public String getComment() { return comment; }
        public void setComment(String comment) { this.comment = comment; }
        public String getTemplateGroupName() { return templateGroupName; }
        public void setTemplateGroupName(String templateGroupName) { this.templateGroupName = templateGroupName; }
        public List<ColumnInfo> getFullColumn() { return fullColumn; }
        public void setFullColumn(List<ColumnInfo> fullColumn) { this.fullColumn = fullColumn; }
        public List<ColumnInfo> getPkColumn() { return pkColumn; }
        public void setPkColumn(List<ColumnInfo> pkColumn) { this.pkColumn = pkColumn; }
        public List<ColumnInfo> getOtherColumn() { return otherColumn; }
        public void setOtherColumn(List<ColumnInfo> otherColumn) { this.otherColumn = otherColumn; }
        public String getSavePackageName() { return savePackageName; }
        public void setSavePackageName(String savePackageName) { this.savePackageName = savePackageName; }
        public String getSavePath() { return savePath; }
        public void setSavePath(String savePath) { this.savePath = savePath; }
        public String getSaveModelName() { return saveModelName; }
        public void setSaveModelName(String saveModelName) { this.saveModelName = saveModelName; }
    }

    public static class ColumnInfo {
        private ObjInfo obj = new ObjInfo();
        private String name;
        private String comment;
        private String type;
        private String shortType;
        private Map<String, Object> ext = new LinkedHashMap<>();

        public ObjInfo getObj() { return obj; }
        public void setObj(ObjInfo obj) { this.obj = obj; }
        public String getName() { return name; }
        public void setName(String name) { this.name = name; }
        public String getComment() { return comment; }
        public void setComment(String comment) { this.comment = comment; }
        public String getType() { return type; }
        public void setType(String type) { this.type = type; }
        public String getShortType() { return shortType; }
        public void setShortType(String shortType) { this.shortType = shortType; }
        public Map<String, Object> getExt() { return ext; }
        public void setExt(Map<String, Object> ext) { this.ext = ext; }
    }

    public static class ObjInfo {
        private String name;
        private DataTypeInfo dataType = new DataTypeInfo();
        private ObjInfo parent;

        public ObjInfo() {
        }

        public String getName() { return name; }
        public void setName(String name) { this.name = name; }
        public DataTypeInfo getDataType() { return dataType; }
        public void setDataType(DataTypeInfo dataType) { this.dataType = dataType; }
        public ObjInfo getParent() { return parent; }
        public void setParent(ObjInfo parent) { this.parent = parent; }
    }

    public static class DataTypeInfo {
        private String typeName;

        public String getTypeName() { return typeName; }
        public void setTypeName(String typeName) { this.typeName = typeName; }
    }
}
