/**
 * ComfyUI 批量场景生成脚本
 * 
 * 使用方法：
 * 1. 在浏览器控制台或 JS evaluate 中运行
 * 2. 传入场景配置数组
 * 
 * 示例：
 *   const scenes = [
 *     { name: "scene1", prompt: "A rainy cityscape at night", image: "ref.png" },
 *     { name: "scene2", prompt: "Close-up face", image: "ref.png" },
 *   ];
 *   for (const scene of scenes) {
 *     await configureScene(scene);
 *     // 点击 Run
 *   }
 */

async function reloadWorkflow() {
  const resp = await fetch("/api/view?filename=LTX-2.3_T2V_I2V_Single_Stage_Distilled_Full.json&subfolder=&type=input");
  if (!resp.ok) throw new Error("Failed to fetch workflow: " + resp.status);
  const wf = await resp.json();
  window.app.loadGraphData(wf);
  await new Promise(r => setTimeout(r, 1500)); // 等待图稳定
  return "Workflow loaded";
}

async function configureScene({ name, prompt, image, steps = 15, frames = 72 }) {
  const graph = window.app.graph;
  const changes = [];

  for (const node of graph._nodes) {
    // 正面提示词
    if (node.id === 2483) {
      for (const w of (node.widgets || [])) {
        if (w.name === "text") { w.value = prompt; changes.push("Prompt set"); }
      }
    }
    
    // Scheduler 参数
    if (node.id === 4966) {
      for (const w of (node.widgets || [])) {
        if (w.name === "steps") { w.value = steps; changes.push(`Steps → ${steps}`); }
        if (w.name === "length") { w.value = frames; changes.push(`Frames → ${frames}`); }
      }
    }
    
    // 输入参考图
    if (node.id === 2004) {
      for (const w of (node.widgets || [])) {
        if (w.name === "image") { w.value = image; changes.push(`Input → ${image}`); }
      }
      node.mode = 0; // 确保启用
    }
    
    // 输出文件名
    if (node.type === "SaveVideo") {
      for (const w of (node.widgets || [])) {
        if (w.name === "filename_prefix") { w.value = name; changes.push(`Output → ${name}`); }
      }
    }
  }

  return changes.join(", ");
}

// 导出供外部使用
if (typeof window !== 'undefined') {
  window.comfyui_batch = { reloadWorkflow, configureScene };
}
