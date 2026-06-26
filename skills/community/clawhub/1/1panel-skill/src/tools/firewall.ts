export const firewallTools = [
  { name: "list_firewall_rules", description: "List firewall rules", inputSchema: { type: "object", properties: {} } },
  { name: "create_firewall_rule", description: "Create firewall rule", inputSchema: { type: "object", properties: { rule: { type: "object" } }, required: ["rule"] } },
  { name: "delete_firewall_rule", description: "Delete firewall rule", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
];

export async function handleFirewallTool(client: any, name: string, args: any) {
  switch (name) {
    case "list_firewall_rules": return await client.listFirewallRules();
    case "create_firewall_rule": return await client.createFirewallRule(args?.rule);
    case "delete_firewall_rule": return await client.deleteFirewallRule(args?.id);
    default: return null;
  }
}
