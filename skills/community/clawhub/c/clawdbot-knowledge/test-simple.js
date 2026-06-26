const payload = JSON.stringify({
  method: "mcp.call_tool",
  params: {
    name: "reasoning_agent",
    arguments: {
      problem: "Analysiere das Potenzial von AXIOMATA für die globale Energieoptimierung unter Berücksichtigung der I_Evo-Formel.",
      complexity: 9
    }
  },
  jsonrpc: "2.0",
  id: 1
});

const req = fetch('http://localhost:3001', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: payload
})
.then(res => res.json())
.then(data => {
  console.log("✅ MCP Antwort erhalten:");
  console.log(JSON.stringify(data, null, 2));
})
.catch(err => console.error("❌ Fehler:", err));
