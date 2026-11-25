"""Check an authored table identity against its cited CREATE TABLE declaration."""


def ddl_primary_key_issues(dataset, table):
    properties = dataset.get("properties", {})
    declared = properties.get("primary_key")
    if properties.get("primary_key_invalid") or (table and table.get("primary_key_invalid")):
        reason = "invalid_declaration"
    elif table and table.get("unreadable_declaration") and declared:
        reason = "unreadable_declaration"
    elif table and "pk_guess" in table and declared is not None and declared != table["pk_guess"]:
        reason = "key_mismatch"
    else:
        return []
    return [{"code": "INVALID_DECLARED_PRIMARY_KEY", "asset_id": dataset["id"], "reason": reason,
             "field": "primary_key", "model_key": declared, "source_key": (table or {}).get("pk_guess"),
             "message": f"{dataset['name']} 的主键与建表原文无法核对，请检查列名、顺序与分隔符，再重新导入或更正。 / Check the primary key against the source DDL."}]
