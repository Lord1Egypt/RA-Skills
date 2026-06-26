#!/usr/bin/env python3
"""
Flutter Hive 数据库代码生成器（JSON 存储模式）

三种独立模式：
  service    → 创建 lib/service/hive_service.dart + hive_repository.dart
  repository → 创建 lib/<feature>/database/<name>_repository.dart
  model      → 创建 lib/<feature>/database/models/<name>_model.dart
               并向对应 Repository 注入 CRUD 方法

用法：
  python generate.py --mode service    --project <path>
  python generate.py --mode repository --project <path> --feature <path> --name <Name>
  python generate.py --mode model      --project <path> --feature <path> --entity '<json>'

安全约束：
- --project 必须是 Flutter 项目根目录（包含 pubspec.yaml 和 lib/）
- --feature 只允许相对 lib 的子路径，不支持 .. 或绝对路径
- --name 只允许 PascalCase 标识符（如 User、TaskRecord）
- --entity 需为合法 JSON，字段结构按照文档约定
"""

import argparse
import json
import re
import sys
from pathlib import Path

# ─── 类型与输入校验辅助 ────────────────────────────────────────────────────────


def nullable_suffix(f):
    return "?" if f.get("nullable", True) else ""


def to_json_expr(f):
    name, t, nullable = f["name"], f["type"], f.get("nullable", True)
    if t == "DateTime":
        return f"{name}{'?.toIso8601String()' if nullable else '.toIso8601String()'}"
    return name

def from_json_expr(f):
    name, t, nullable = f["name"], f["type"], f.get("nullable", True)
    if t == "DateTime":
        if nullable:
            return f"json['{name}'] != null ? DateTime.parse(json['{name}'] as String) : null"
        return f"DateTime.parse(json['{name}'] as String)"
    if t == "double":
        if nullable:
            return f"json['{name}'] != null ? (json['{name}'] as num).toDouble() : null"
        return f"(json['{name}'] as num).toDouble()"
    cast = f" as {t}{'?' if nullable else ''}"
    return f"json['{name}']{cast}"

def _camel(name):
    return name[0].lower() + name[1:] if name else name


def _snake(name):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def _plural(name):
    return name + "s" if not name.endswith("s") else name


def _validate_project_root(project_path: str) -> Path:
    """校验并返回项目根目录，防止写入到非 Flutter 项目路径。"""
    root = Path(project_path).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        print(f"[错误] 项目路径不存在或不是目录: {root}")
        sys.exit(1)
    pubspec = root / "pubspec.yaml"
    lib_dir = root / "lib"
    if not pubspec.exists() or not lib_dir.exists():
        print(f"[错误] 目标目录不是有效的 Flutter 项目（缺少 pubspec.yaml 或 lib/）: {root}")
        sys.exit(1)
    return root


def _validate_feature(feature: str) -> str:
    """校验 feature 路径，仅允许 lib 下的相对子路径，防止路径穿越。"""
    feat = feature.strip().strip("/ ")
    if not feat:
        print("[错误] --feature 不能为空")
        sys.exit(1)
    if ".." in feat or feat.startswith(("/", "\\")):
        print(f"[错误] 非法的 feature 路径（不允许 .. 或绝对路径）: {feature!r}")
        sys.exit(1)
    if not re.fullmatch(r"[A-Za-z0-9_/]+", feat):
        print(f"[错误] 非法的 feature 路径，仅支持字母/数字/下划线/斜杠: {feature!r}")
        sys.exit(1)
    return feat


def _validate_name(name: str) -> str:
    """校验 Repository / Model 名称（PascalCase），防止注入。"""
    n = name.strip()
    if not re.fullmatch(r"[A-Z][A-Za-z0-9_]*", n):
        print(f"[错误] 非法的名称: {name!r}，需为 PascalCase（如 User、TaskRecord）")
        sys.exit(1)
    return n


def _get_package_name(project_root: Path) -> str:
    pubspec = project_root / "pubspec.yaml"
    if not pubspec.exists():
        print(f"[错误] 未找到 pubspec.yaml: {pubspec}")
        sys.exit(1)
    for line in pubspec.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("name:"):
            return line.split(":", 1)[1].strip()
    print("[错误] pubspec.yaml 中未找到 name 字段")
    sys.exit(1)


def _write(path: Path, content: str, overwrite=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        print(f"  ⏭️   已存在跳过: {path}")
        return False
    path.write_text(content, encoding="utf-8")
    print(f"  ✅  {'更新' if path.exists() else '创建'}: {path}")
    return True

# ─── 模式 1：service ──────────────────────────────────────────────────────────

def gen_hive_service():
    return """\
import 'package:hive_ce_flutter/hive_flutter.dart';

/// Hive 初始化与 Box 管理（懒加载，无需注册 TypeAdapter）
/// 所有数据以 JSON Map 格式存储，无类型数量上限
class HiveService {
  static final Map<String, Box<Map>> _boxes = {};

  /// [subDir] 可选，指定数据库存储子目录（相对于应用文档目录）
  /// 例如：`HiveService.init(subDir: 'db')` → <documents>/db/
  static Future<void> init({String? subDir}) async {
    await Hive.initFlutter(subDir);
  }

  /// 懒加载打开 Box，已打开则直接返回
  static Future<Box<Map>> openBox(String boxName) async {
    if (_boxes[boxName]?.isOpen == true) return _boxes[boxName]!;
    _boxes[boxName] = await Hive.openBox<Map>(boxName);
    return _boxes[boxName]!;
  }

  static Future<void> closeAll() async {
    for (final box in _boxes.values) {
      if (box.isOpen) await box.close();
    }
    _boxes.clear();
  }
}
"""

def gen_hive_repository():
    return """\
import 'package:hive_ce_flutter/hive_flutter.dart';

/// 通用 Hive Repository 基类（JSON Map 存储模式）
/// 子类实现 box、toJson、fromJson 三个成员即可获得完整 CRUD 能力
abstract class HiveRepository<T> {
  Future<Box<Map>> get box;

  Map<String, dynamic> toJson(T value);
  T fromJson(Map<dynamic, dynamic> json);

  Future<void> put(String key, T value) async =>
      (await box).put(key, toJson(value));

  Future<void> putAll(Map<String, T> entries) async =>
      (await box).putAll(entries.map((k, v) => MapEntry(k, toJson(v))));

  Future<T?> get(String key) async {
    final map = (await box).get(key);
    return map != null ? fromJson(map) : null;
  }

  Future<List<T>> getAll() async =>
      (await box).values.map((m) => fromJson(m)).toList();

  Future<void> delete(String key) async => (await box).delete(key);

  Future<void> deleteAll(Iterable<String> keys) async =>
      (await box).deleteAll(keys);

  Future<void> clear() async => (await box).clear();

  Future<bool> containsKey(String key) async =>
      (await box).containsKey(key);

  Future<int> get length async => (await box).length;
}
"""

def cmd_service(project: str):
    root = _validate_project_root(project)
    pkg = _get_package_name(root)
    service_dir = root / "lib" / "service"
    print(f"\n📦  项目: {pkg}")
    print(f"📂  目标目录: {service_dir}\n")
    _write(service_dir / "hive_service.dart", gen_hive_service())
    _write(service_dir / "hive_repository.dart", gen_hive_repository())
    print("\n📌  请在 main.dart 添加：\n")
    print(f"  import 'package:{pkg}/service/hive_service.dart';")
    print("  await HiveService.init();  // 在 runApp() 之前\n")

# ─── 模式 2：repository ───────────────────────────────────────────────────────

def gen_entity_repository(name: str, pkg: str) -> str:
    snake = _snake(name)
    box_name = _plural(snake)
    return f"""\
import 'package:hive_ce_flutter/hive_flutter.dart';
import 'package:{pkg}/service/hive_service.dart';

/// {name} 数据库操作
/// 运行 generate.py --mode model 后将自动注入对应 Model 的 CRUD 方法
class {name}DatabaseRepository {{
  static const _boxName = '{box_name}';

  Future<Box<Map>> get _box => HiveService.openBox(_boxName);

  /// 原始 Map 存储（临时使用，建议通过 Model CRUD 方法操作）
  Future<void> putRaw(String key, Map<String, dynamic> data) async =>
      (await _box).put(key, data);

  Future<Map<dynamic, dynamic>?> getRaw(String key) async =>
      (await _box).get(key);

  Future<List<Map>> getAllRaw() async =>
      (await _box).values.toList();

  Future<void> delete(String key) async => (await _box).delete(key);

  Future<void> clear() async => (await _box).clear();

  Future<int> get length async => (await _box).length;
}}
"""

def cmd_repository(project: str, feature: str, name: str):
    root = _validate_project_root(project)
    feat = _validate_feature(feature)
    name = _validate_name(name)
    pkg = _get_package_name(root)
    snake = _snake(name)
    db_dir = root / "lib" / feat / "database"
    repo_file = db_dir / f"{snake}_repository.dart"
    print(f"\n📦  项目: {pkg}  功能模块: {feature}")
    print(f"📂  目标目录: {db_dir}\n")
    _write(repo_file, gen_entity_repository(name, pkg))
    print(f"\n✅  Repository 已创建！可通过以下命令添加 Model：")
    print(f"  python generate.py --mode model --project {project} --feature {feature} --entity '<json>'\n")

# ─── 模式 3：model ────────────────────────────────────────────────────────────

def gen_model(entity: dict) -> str:
    name = entity["name"]
    fields = entity["fields"]

    fields_code = "".join(
        f"  final {f['type']}{nullable_suffix(f)} {f['name']};\n" for f in fields
    )
    ctor_params = "\n".join(
        f"    {'this' if f.get('nullable', True) else 'required this'}.{f['name']},"
        for f in fields
    )
    to_json_lines = ",\n".join(
        f"      '{f['name']}': {to_json_expr(f)}" for f in fields
    )
    from_json_lines = ",\n".join(
        f"      {f['name']}: {from_json_expr(f)}" for f in fields
    )
    copy_with_params = ", ".join(
        f"{f['type']}{'?' if f.get('nullable', True) else '?'} {f['name']}"
        for f in fields
    )
    copy_with_body = ",\n      ".join(
        f"{f['name']}: {f['name']} ?? this.{f['name']}" for f in fields
    )
    to_str = ", ".join(f"{f['name']}: ${{{f['name']}}}" for f in fields)
    eq_body = " && ".join(f"other.{f['name']} == {f['name']}" for f in fields)
    hash_body = (f"Object.hash({', '.join(f['name'] for f in fields)})"
                 if len(fields) > 1 else f"{fields[0]['name']}.hashCode")

    return f"""\
/// {name} 数据模型
/// 存储策略：toJson() → Hive Box<Map> → fromJson()，无需 TypeAdapter
class {name}Model {{
{fields_code}
  const {name}Model({{
{ctor_params}
  }});

  Map<String, dynamic> toJson() => {{
{to_json_lines}
    }};

  factory {name}Model.fromJson(Map<dynamic, dynamic> json) => {name}Model(
{from_json_lines}
    );

  {name}Model copyWith({{{copy_with_params}}}) => {name}Model(
      {copy_with_body},
    );

  @override
  String toString() => '{name}({to_str})';

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is {name}Model && {eq_body};

  @override
  int get hashCode => {hash_body};
}}
"""

def gen_crud_methods(entity: dict, pkg: str, feature: str) -> str:
    """生成注入到 Repository 的 CRUD 方法块"""
    name = entity["name"]
    snake = _snake(name)
    camel = _camel(name)
    fields = entity["fields"]
    id_field = next((f for f in fields if f["name"] == "id"), fields[0] if fields else None)
    id_type = id_field["type"] if id_field else "String"
    model_import = f"models/{snake}_model.dart"

    return f"""\

  // ── {name}Model CRUD ────────────────────────────────────────────────────────

  /// 保存（以 id 为 key 覆盖写入）
  Future<void> save{name}({name}Model model) async =>
      (await _box).put(model.{id_field['name'] if id_field else 'id'}.toString(), model.toJson());

  /// 按 id 查询，不存在返回 null
  Future<{name}Model?> find{name}ById({id_type} id) async {{
    final map = (await _box).get(id.toString());
    return map != null ? {name}Model.fromJson(map) : null;
  }}

  /// 查询全部 {name}
  Future<List<{name}Model>> getAll{name}s() async =>
      (await _box).values.map((m) => {name}Model.fromJson(m)).toList();

  /// 更新（等同于 save，key 存在则覆盖）
  Future<void> update{name}({name}Model model) async =>
      save{name}(model);

  /// 按 id 删除
  Future<void> delete{name}ById({id_type} id) async =>
      (await _box).delete(id.toString());
"""

def _inject_import(content: str, import_line: str) -> str:
    """在最后一个 import 行后插入新 import（若不存在）"""
    if import_line in content:
        return content
    lines = content.splitlines()
    last_import = max(
        (i for i, l in enumerate(lines) if l.strip().startswith("import ")),
        default=-1,
    )
    insert_at = last_import + 1 if last_import >= 0 else 0
    lines.insert(insert_at, import_line)
    return "\n".join(lines)

def _inject_crud(repo_file: Path, entity: dict, pkg: str, feature: str) -> bool:
    """向 Repository 文件注入 CRUD 方法及 Model import，返回是否成功"""
    name = entity["name"]
    snake = _snake(name)

    if not repo_file.exists():
        print(f"  ⚠️  Repository 文件不存在：{repo_file}")
        print(f"      请先执行 --mode repository 创建 Repository")
        return False

    content = repo_file.read_text(encoding="utf-8")

    if f"save{name}(" in content:
        print(f"  ⏭️   {name}Model CRUD 已存在，跳过注入")
        return True

    # 注入 import
    import_line = f"import 'models/{snake}_model.dart';"
    content = _inject_import(content, import_line)

    # 找最后一个 } 注入 CRUD
    last_brace = content.rfind("}")
    if last_brace == -1:
        print(f"  ❌  无法解析 Repository 文件（未找到类结尾 '}}' ）")
        return False

    crud = gen_crud_methods(entity, pkg, feature)
    new_content = content[:last_brace] + crud + "}\n"
    repo_file.write_text(new_content, encoding="utf-8")
    print(f"  ✅  CRUD 方法已注入: {repo_file}")
    return True

def cmd_model(project: str, feature: str, entity: dict):
    root = _validate_project_root(project)
    feat = _validate_feature(feature)
    pkg = _get_package_name(root)
    name = entity["name"]
    snake = _snake(name)
    db_dir = root / "lib" / feat / "database"
    models_dir = db_dir / "models"
    repo_file = db_dir / f"{snake}_repository.dart"

    print(f"\n📦  项目: {pkg}  功能模块: {feature}  实体: {name}\n")

    # 创建 Model 文件
    _write(models_dir / f"{snake}_model.dart", gen_model(entity))

    # 向 Repository 注入 CRUD
    print("注入 CRUD 方法到 Repository...")
    if not _inject_crud(repo_file, entity, pkg, feature):
        # Repository 不存在时，自动创建并注入
        print(f"  ℹ️   自动创建 Repository 并写入 CRUD...")
        _write(repo_file, gen_entity_repository(name, pkg))
        _inject_crud(repo_file, entity, pkg, feature)

    print(f"\n✅  完成！目录结构：")
    print(f"  {db_dir}/")
    print(f"  ├── {snake}_repository.dart")
    print(f"  └── models/")
    print(f"      └── {snake}_model.dart\n")

# ─── 主入口 ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Flutter Hive 代码生成器（带安全校验）")
    parser.add_argument("--mode", required=True,
                        choices=["service", "repository", "model"],
                        help="service | repository | model")
    parser.add_argument("--project", required=True, help="Flutter 项目根目录绝对路径")
    parser.add_argument("--feature", default="", help="功能模块路径（从 lib/ 开始，如 features/user）")
    parser.add_argument("--name",    default="", help="[repository 模式] Repository 类名（PascalCase）")
    parser.add_argument("--entity",  default="", help="[model 模式] 实体 JSON 字符串")
    args = parser.parse_args()

    try:
        if args.mode == "service":
            cmd_service(args.project)

        elif args.mode == "repository":
            if not args.feature or not args.name:
                print("[错误] --mode repository 需要 --feature 和 --name 参数")
                sys.exit(1)
            cmd_repository(args.project, args.feature, args.name)

        elif args.mode == "model":
            if not args.feature or not args.entity:
                print("[错误] --mode model 需要 --feature 和 --entity 参数")
                sys.exit(1)
            try:
                entity = json.loads(args.entity)
            except json.JSONDecodeError as e:
                print(f"[错误] --entity 不是合法 JSON: {e}")
                sys.exit(1)
            if not isinstance(entity, dict) or "name" not in entity or "fields" not in entity:
                print("[错误] --entity JSON 结构非法，需包含 name 和 fields 字段")
                sys.exit(1)
            cmd_model(args.project, args.feature, entity)
    except KeyboardInterrupt:
        print("\n已中断")
        sys.exit(130)


if __name__ == "__main__":
    main()
