"""Finite export-structure checks; no execution and no universal schema claim."""
def check(nodes, edges, baseline=None):
    findings = []
    def add(code, node, message, severity="error"):
        findings.append(dict(code=code, severity=severity, message=message, node_id=node.get("nodeId", ""), path="$.nodes", suggested_fix="核对目标实例基线和回读，不猜测节点结构"))
    aliases = {"switch": "ifElseNode"}
    wrong = {"system_httpReqTimeout": "system_httpTimeout", "system_httpHeaderContentType": "system_httpContentType", "system_http_raw_response": "httpRawResponse", "switchList": "ifElseList"}
    known = {n.get("flowNodeType") for n in (baseline or {}).get("nodes", [])}
    for node in nodes:
        kind = node.get("flowNodeType")
        nid = node.get("nodeId", "")
        inputs = {i.get("key"): i for i in node.get("inputs", []) if isinstance(i, dict)}
        outputs = {i.get("key") for i in node.get("outputs", []) if isinstance(i, dict)}
        if kind in aliases and kind not in known:
            add("FG090", node, "缺少目标基线依据的节点类型：" + kind + "；常见导出为" + aliases[kind])
        elif known and kind not in known:
            add("FG090", node, "目标schema基线未包含该节点类型；需补目标导出证据", "warning")
        for key in set(inputs) | outputs:
            if key in wrong:
                add("FG091", node, "疑似误写节点键：" + key + "；核对" + wrong[key])
        if kind == "ifElseNode":
            groups = inputs.get("ifElseList", {}).get("value")
            if not isinstance(groups, list) or not groups:
                add("FG092", node, "条件节点缺少非空ifElseList")
            else:
                expected = {nid + "-source-IF", nid + "-source-ELSE"} | {nid + "-source-ELSE IF " + str(i) for i in range(1, len(groups))}
                # Explicit branchId changes handle derivation; do not impose label rules.
                if not any(isinstance(g, dict) and g.get("branchId") for g in groups):
                    actual = {e.get("sourceHandle") for e in edges if e.get("source") == nid and "source_catch" not in e.get("sourceHandle", "")}
                    if actual != expected:
                        add("FG092", node, "条件出口handle与条件组数量不一致（标签式基线）")
        catch = [e for e in edges if e.get("source") == nid and "source_catch" in e.get("sourceHandle", "")]
        if catch and not node.get("catchError"):
            add("FG093", node, "存在catch边但节点未启用catchError")
        if kind == "httpRequest468":
            for key in ("system_httpReqUrl", "system_httpMethod"):
                if key not in inputs:
                    add("FG094", node, "HTTP节点缺少输入键：" + key)
            if node.get("catchError") and not catch:
                add("FG093", node, "HTTP已启用catch但没有异常出口边", "warning")
    from execution_binding_checks import check as check_bindings
    findings.extend(check_bindings(nodes, baseline))
    return findings
