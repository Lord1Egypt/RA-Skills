const payload = JSON.stringify({
  jsonrpc: "2.0",
  id: 1,
  method: "tools/call",
  params: {
    name: "reasoning_agent",
    arguments: {
      problem: "Analysiere das Potenzial von AXIOMATA für die globale Energieoptimierung unter Berücksichtigung der I_Evo-Formel.",
      complexity: 9
    }
  }
});

fetch('http://localhost:3001', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: payload
})
.then(res => res.text().then(text => {
  console.log("Status:", res.status);
  console.log("Raw Response:", text);
  try {
     return JSON.parse(text);
  } catch(e) { return {error: "Failed to parse JSON", raw: text}; }
}))
.then(data => console.log("Data:", JSON.stringify(data, null, 2)))
.catch(err => console.error("Fetch Error:", err));
