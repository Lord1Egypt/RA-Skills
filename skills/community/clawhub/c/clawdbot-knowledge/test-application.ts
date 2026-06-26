import axios from 'axios';

async function testMcp() {
  console.log("🚀 Starte praktischen Test des MCP Orchestral Systems...");
  
  const payload = {
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
  };

  try {
    const response = await axios.post('http://localhost:3001', payload);
    console.log("✅ Antwort vom Reasoning Agent erhalten:");
    console.log(JSON.stringify(response.data, null, 2));
  } catch (error) {
    console.error("❌ Fehler beim Aufruf des Tools:", error.message);
  }
}

testMcp();
