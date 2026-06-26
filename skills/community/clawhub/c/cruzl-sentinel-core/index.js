// 🔥 Cruzl Sentinel Core - FINAL VERSION

function scoreProject(name) {
  const base = {
    "soneium": 85,
    "ink": 80,
    "litvm": 78,
    "base": 82
  };

  const variation = Math.floor(Math.random() * 10) - 5; // -5 to +4
  return Math.max(50, (base[name.toLowerCase()] || 70) + variation);
}

function generateStrategy(score) {
  if (score >= 85) {
    return "High priority: interact 3-5x/week, varied tx size, multi-dApp usage.";
  }
  if (score >= 75) {
    return "Medium priority: interact 1-2x/week with moderate volume.";
  }
  return "Low priority: light interaction, maintain presence only.";
}

function extractProject(query) {
  const projects = ["soneium", "ink", "litvm", "base"];
  return projects.find(p => query.includes(p)) || null;
}

async function run(input) {
  const query = input?.query?.toLowerCase() || "";

  // 🔍 SCAN MODE
  if (query.includes("scan")) {
    return ["soneium", "ink", "litvm", "base"].map(p => ({
      name: p,
      score: scoreProject(p)
    }));
  }

  // 🎯 STRATEGY MODE
  if (query.includes("strategy")) {
    const project = extractProject(query) || "soneium";
    const score = scoreProject(project);

    return {
      project,
      score,
      strategy: generateStrategy(score)
    };
  }

  // 💰 WALLET MODE
  const walletMatch = query.match(/0x[a-f0-9]{40}/);
  if (walletMatch) {
    const score = Math.floor(Math.random() * 100);

    return {
      address: walletMatch[0],
      activityScore: score,
      insight:
        score > 70
          ? "Active wallet. Maintain diversified interactions."
          : "Low activity. Increase interaction frequency."
    };
  }

  // ❓ DEFAULT
  return {
    message: "Try: scan / strategy for soneium / paste wallet"
  };
}

// 🔥 CLI TEST MODE
if (process.argv[2]) {
  const input = { query: process.argv[2] };

  run(input).then(res => {
    console.log(JSON.stringify(res, null, 2));
  });
}

// 🔗 EXPORT FOR CLAWHUB
module.exports = { run };