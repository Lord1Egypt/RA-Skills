document.addEventListener("DOMContentLoaded", () => {
  const statAgents = document.getElementById("stat-agents");
  const statClusters = document.getElementById("stat-clusters");
  const statTokens = document.getElementById("stat-tokens");
  const statSavings = document.getElementById("stat-savings");
  const agentsContainer = document.getElementById("agents-container");
  const clustersContainer = document.getElementById("clusters-container");
  const btnRefresh = document.getElementById("btn-refresh");
  const btnTrigger = document.getElementById("btn-trigger-cycle");
  const routingForm = document.getElementById("routing-form");
  const promptInput = document.getElementById("prompt-input");
  const resultBox = document.getElementById("result-box");
  const resultJson = document.getElementById("result-json");
  const resultBadge = document.getElementById("result-source-badge");
  const resultLatency = document.getElementById("result-latency");
  const meshNodesCount = document.getElementById("mesh-nodes-count");

  const canvas = document.getElementById("mesh-canvas");
  const ctx = canvas ? canvas.getContext("2d") : null;

  let currentAgents = [];
  let currentClusters = [];
  let particles = [];

  // Resize Canvas to device pixel ratio
  function resizeCanvas() {
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * window.devicePixelRatio;
    canvas.height = rect.height * window.devicePixelRatio;
    ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
  }
  window.addEventListener("resize", resizeCanvas);
  resizeCanvas();

  // Draw Topology Mesh
  function drawMesh() {
    if (!ctx || !canvas) return;
    const width = canvas.getBoundingClientRect().width;
    const height = canvas.getBoundingClientRect().height;

    ctx.clearRect(0, 0, width, height);

    // Center Node: Orchestrator
    const centerX = width / 2;
    const centerY = height / 2;

    // Draw background grid lines
    ctx.strokeStyle = "rgba(255, 255, 255, 0.03)";
    ctx.lineWidth = 1;
    for (let r = 40; r < Math.min(width, height) / 2; r += 45) {
      ctx.beginPath();
      ctx.arc(centerX, centerY, r, 0, Math.PI * 2);
      ctx.stroke();
    }

    // Connect to Subagents
    const totalNodes = currentAgents.length + currentClusters.length;
    let nodeIndex = 0;

    currentAgents.forEach((agent, i) => {
      const angle = (nodeIndex / (totalNodes || 1)) * Math.PI * 2;
      const dist = Math.min(width, height) * 0.35;
      const x = centerX + Math.cos(angle) * dist;
      const y = centerY + Math.sin(angle) * dist;

      // Connecting line
      ctx.strokeStyle = "rgba(6, 182, 212, 0.3)";
      ctx.lineWidth = 2;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.lineTo(x, y);
      ctx.stroke();
      ctx.setLineDash([]);

      // Subagent Node
      ctx.fillStyle = "#06b6d4";
      ctx.beginPath();
      ctx.arc(x, y, 14, 0, Math.PI * 2);
      ctx.fill();
      ctx.shadowColor = "#06b6d4";
      ctx.shadowBlur = 12;

      ctx.fillStyle = "#ffffff";
      ctx.font = "10px JetBrains Mono, monospace";
      ctx.textAlign = "center";
      ctx.fillText(agent.target_domain || agent.agent_id, x, y + 26);

      nodeIndex++;
    });

    // Connect to Emerging Clusters
    currentClusters.forEach((cluster, i) => {
      const angle = (nodeIndex / (totalNodes || 1)) * Math.PI * 2;
      const dist = Math.min(width, height) * 0.38;
      const x = centerX + Math.cos(angle) * dist;
      const y = centerY + Math.sin(angle) * dist;

      // Line to cluster
      ctx.strokeStyle = "rgba(139, 92, 246, 0.25)";
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.lineTo(x, y);
      ctx.stroke();

      // Cluster Node
      ctx.fillStyle = cluster.eligible ? "#f59e0b" : "#8b5cf6";
      ctx.beginPath();
      ctx.arc(x, y, 10, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = "#9ca3af";
      ctx.font = "9px Inter, sans-serif";
      ctx.textAlign = "center";
      ctx.fillText(cluster.domain_tag, x, y + 20);

      nodeIndex++;
    });

    // Draw Orchestrator Center Node
    ctx.shadowColor = "#8b5cf6";
    ctx.shadowBlur = 20;
    ctx.fillStyle = "#8b5cf6";
    ctx.beginPath();
    ctx.arc(centerX, centerY, 22, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 11px Inter, sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("⚡ ORCHESTRATOR", centerX, centerY + 4);

    // Animate Pulses / Particles
    particles.forEach((p, idx) => {
      p.t += 0.02;
      const px = centerX + (p.targetX - centerX) * p.t;
      const py = centerY + (p.targetY - centerY) * p.t;

      ctx.fillStyle = p.color || "#06b6d4";
      ctx.beginPath();
      ctx.arc(px, py, 4, 0, Math.PI * 2);
      ctx.fill();

      if (p.t >= 1) particles.splice(idx, 1);
    });

    requestAnimationFrame(drawMesh);
  }

  // Load Dashboard Data
  async function loadOverview() {
    try {
      const res = await fetch("/api/overview");
      if (!res.ok) throw new Error("Network error");
      const data = await res.json();

      currentAgents = data.agents || [];
      currentClusters = data.clusters || [];

      // Update counters
      statAgents.textContent = data.active_subagents_count;
      statClusters.textContent = data.discovered_clusters_count;
      statTokens.textContent = data.tokens_saved.toLocaleString();

      if (statSavings && data.finops) {
        statSavings.textContent = `$${data.finops.total_dollars_saved} (${data.finops.total_euros_saved} €)`;
      }

      if (meshNodesCount) {
        meshNodesCount.textContent = `Orchestrator + ${currentAgents.length} Sub-Agent(s)`;
      }

      // Render Agents
      if (currentAgents.length > 0) {
        agentsContainer.innerHTML = currentAgents.map(a => `
          <div class="agent-item">
            <div class="agent-item-title">
              <span>🛡️ ${a.agent_id}</span>
              <span class="badge badge-success">${a.version} • ${a.status}</span>
            </div>
            <div class="agent-meta">
              <span>Domain: <strong>${a.target_domain}</strong></span>
              <span>Tools: ${a.allowed_tools.map(t => `<span class="tool-tag">${t}</span>`).join(" ")}</span>
            </div>
          </div>
        `).join("");
      } else {
        agentsContainer.innerHTML = `<div class="empty-state">No active sub-agents yet (Ready for real production tasks).</div>`;
      }

      // Render Clusters
      if (currentClusters.length > 0) {
        clustersContainer.innerHTML = currentClusters.map(c => `
          <div class="cluster-item">
            <div class="agent-item-title">
              <span>🧬 ${c.domain_tag}</span>
              <span class="badge ${c.eligible ? 'badge-warning' : 'badge-info'}">
                ${c.eligible ? 'ELIGIBLE FOR FACTORY' : 'MONITORING'}
              </span>
            </div>
            <div class="agent-meta">
              <span>Occurrences: ${c.occurrences}</span>
              <span>Score: ${c.composite_score}</span>
              <span>Errors: ${(c.error_rate * 100).toFixed(0)}%</span>
            </div>
          </div>
        `).join("");
      } else {
        clustersContainer.innerHTML = `<div class="empty-state">Awaiting incoming telemetry logs...</div>`;
      }
    } catch (err) {
      console.error("Dashboard loading error:", err);
    }
  }

  // Routing test form submission
  routingForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const prompt = promptInput.value.trim();
    if (!prompt) return;

    if (canvas && currentAgents.length > 0) {
      const width = canvas.getBoundingClientRect().width;
      const height = canvas.getBoundingClientRect().height;
      particles.push({
        t: 0,
        targetX: width / 2 + Math.cos(0.5) * (width * 0.35),
        targetY: height / 2 + Math.sin(0.5) * (height * 0.35),
        color: "#06b6d4"
      });
    }

    const startTime = performance.now();
    try {
      const res = await fetch("/api/route", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt })
      });
      const data = await res.json();
      const elapsed = (performance.now() - startTime).toFixed(1);

      resultBox.style.display = "block";
      resultLatency.textContent = `${elapsed} ms`;
      resultJson.textContent = JSON.stringify(data, null, 2);

      if (data.source === "SEMANTIC_CACHE") {
        resultBadge.className = "badge badge-success";
        resultBadge.textContent = "⚡ SEMANTIC CACHE (0 TOKENS)";
      } else if (data.source === "SPECIALIZED_SUBAGENT") {
        resultBadge.className = "badge badge-info";
        resultBadge.textContent = `🤖 SUB-AGENT: ${data.agent_id}`;
      } else {
        resultBadge.className = "badge badge-warning";
        resultBadge.textContent = "🌐 GENERALIST ORCHESTRATOR";
      }

      loadOverview();
    } catch (err) {
      console.error(err);
    }
  });

  // Trigger factory cycle button
  btnTrigger.addEventListener("click", async () => {
    btnTrigger.disabled = true;
    btnTrigger.innerHTML = `<span class="btn-icon">⏳</span> Synthesizing...`;
    try {
      const res = await fetch("/api/trigger-cycle", { method: "POST" });
      const result = await res.json();
      alert(`Factory Cycle Completed!\nStatus: ${result.status}\nSub-Agent: ${result.synthesized?.agent_id || 'No eligible candidate cluster'}`);
      loadOverview();
    } catch (err) {
      alert("Error executing factory cycle");
    } finally {
      btnTrigger.disabled = false;
      btnTrigger.innerHTML = `<span class="btn-icon">⚡</span> Trigger Factory Cycle`;
    }
  });

  btnRefresh.addEventListener("click", loadOverview);

  // Start Animation & Initial load
  drawMesh();
  loadOverview();
});
