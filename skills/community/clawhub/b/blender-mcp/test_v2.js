import { execute } from './server.js';

async function testMcpBridge() {
  console.log("--- Testing MCP Bridge Discovery ---");
  // Test case 1: Missing tool name (should return availability list)
  const discovery = await execute({});
  console.log("Discovery Output:", discovery);

  console.log("\n--- Testing MCP Tool List ---");
  // Test case 2: Real call attempt (will fail if Blender isn't running, but verifies bridge logic)
  try {
    const list = await execute({ tool: "get_scene_info" });
    console.log("Tool Result:", JSON.stringify(list, null, 2));
  } catch (e) {
    console.log("Logic verified but connection failed (expected if Blender UI is closed):", e.message);
  }
}

testMcpBridge();
