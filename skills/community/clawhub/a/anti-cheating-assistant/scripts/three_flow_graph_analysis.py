"""三流图分析法工作流。

main 函数是整个脚本的入口，请保留并不要修改 main 函数的函数名和参数。
"""
import json
from urllib.parse import quote

def main(params: dict):
    """
    分析业务描述，生成三流图和三流表。

    params: 包含
        business_name: 客户自定义的业务名称
        business_step_infos: 标准 JSON 格式的业务流程

    ret: 包含
        business_name：客户自定义的业务名称
        three_flow_graph：生成的业务三流图链接
        three_flow_table：生成的业务三流表，Markdown格式
        business_step_info：业务流程的详细信息
        roles：业务流程中涉及的角色roles
    """
    business_name = params['business_name']
    business_step_infos = params['std_info'] if isinstance(params['std_info'], list) else json.loads(params['std_info'])
    
    # 保持角色顺序为首次出现顺序，以保证表格列和图的一致性
    roles = []
    for step in business_step_infos:
        for r in (step.get('from_role', ''), step.get('to_role', '')):
            if r and r not in roles:
                roles.append(r)
    length = len(roles)
    # 使用 flowchart 表示法，后续以 three_flow_table 为准构造图中的连线和标签
    graph_context = ["graph LR"]
    # three_flow_table 采用 Markdown 表格格式：标题行、分隔行、每个步骤的 C/V 标记。
    # C 表示角色可控，V 表示角色可见。
    table_context = ["||步骤|载体|" + "|".join(roles) + "|", "|--|--|--|" + "--|" * length]
    value_context = []
    # 载体类型映射：
    # 1 = 信息流：数据、指令、确认等信息的传递
    # 2 = 资金流：金钱的流动和结算
    # 3 = 服务流：实际服务/商品的交付
    # 4 = 物流：实物或商品的运输过程
    carrier_table = ["", "信息流", "资金流", "服务流", "物流"]

    for business_step_info in business_step_infos:
        step_no = business_step_info.get('step_no', 0)
        step_name = business_step_info.get('step_name', "")
        carrier = business_step_info.get('carrier', 0)
        from_role = business_step_info.get('from_role', "")
        to_role = business_step_info.get('to_role', "")
        from_controllable = business_step_info.get('from_controllable', False)
        to_controllable = business_step_info.get('to_controllable', False)
        other_visible_roles = business_step_info.get('other_visible_roles', [])
        other_visible_role_string = ",".join(other_visible_roles)
        from_multiple = business_step_info.get('from_multiple', False)
        to_multiple = business_step_info.get('to_multiple', False)
        
        # 使用表中的信息构造 graph 连接，label 使用 步骤号.载体
        label = f"{step_no}.{carrier_table[carrier]}"
        graph_line = f'"{from_role}" -->|"{label}"| "{to_role}"'
        table_line = f"|{step_no}|{step_name}|{carrier_table[carrier]}|"
        # 修复 value_line 中重复使用 to_controllable 的错误，最后一个字段应为 to_multiple
        value_line = f"('{business_name}',{step_no},'{step_name}',{carrier},'{from_role}','{to_role}',{str(from_controllable).lower()},{str(to_controllable).lower()},'{other_visible_role_string}',{str(from_multiple).lower()},{str(to_multiple).lower()})"
        
        for role in roles:
            if (role == from_role and from_controllable) or (role == to_role and to_controllable):
                table_line += "C|"
            elif role == from_role or role == to_role or role in other_visible_roles:
                table_line += "V|"
            else:
                table_line += "|"
                
        graph_context.append(graph_line)
        table_context.append(table_line)
        value_context.append(value_line)
    
    ret = {
        "business_name": business_name,
        # 三流图可视化链接
        "three_flow_graph": f"https://hdconsultatio.com/mermaid.html?business_name={quote(business_name)}&std_info={quote(json.dumps(business_step_infos))}",
        # 三流表格，Markdown 表格结构：标题行、分隔行、每个步骤的 C/V 标记
        "three_flow_table": "\n".join(table_context),
        "business_step_info": ",\n".join(value_context),
        "roles": ",".join(roles)
    }
    
    return ret