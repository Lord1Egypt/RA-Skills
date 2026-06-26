import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import os from "os";

const RPC_URL = "http://localhost:6800/jsonrpc";

// 获取系统默认下载目录
function getDefaultDownloadDir(): string {
  const homeDir = os.homedir();
  const platform = os.platform();
  
  if (platform === "win32") {
    return "C:\\Users\\" + os.userInfo().username + "\\Downloads";
  } else if (platform === "darwin") {
    return "/Users/" + os.userInfo().username + "/Downloads";
  } else {
    // Linux and others
    return homeDir + "/Downloads";
  }
}

async function rpcCall(method: string, params: any[] = []): Promise<any> {
  const { default: fetch } = await import("node-fetch");
  const response = await fetch(RPC_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      jsonrpc: "2.0",
      method,
      params,
      id: Date.now(),
    }),
  });
  const data = await response.json();
  return data.result;
}

const plugin = {
  id: "bt-download",
  name: "BT Download",
  description: "BT下载助手，支持BT文件、磁力链接和普通下载链接，支持RPC模式和自动做种监控",
  async register(api: OpenClawPluginApi) {
    // 检查 aria2 是否安装
    api.registerTool({
      name: "bt_check_aria2",
      description: "检查 aria2 是否已安装，返回安装状态和版本信息",
      inputSchema: { type: "object", properties: {} },
      handler: async () => {
        const { exec } = await import("child_process");
        return new Promise((resolve) => {
          exec("which aria2c && aria2c --version | head -1", (err, stdout) => {
            if (err) {
              resolve({ installed: false, message: "aria2 未安装" });
            } else {
              resolve({ installed: true, version: stdout.trim(), path: "/usr/bin/aria2c" });
            }
          });
        });
      },
    });

    // 安装 aria2
    api.registerTool({
      name: "bt_install_aria2",
      description: "在系统上安装 aria2 下载工具",
      inputSchema: { type: "object", properties: {} },
      handler: async () => {
        const { exec } = await import("child_process");
        return new Promise((resolve) => {
          exec(
            "which aria2c || (sudo apt-get update && sudo apt-get install -y aria2)",
            (err, stdout, stderr) => {
              if (err) {
                resolve({ success: false, message: "安装失败: " + stderr });
              } else {
                resolve({ success: true, message: "aria2 安装成功" });
              }
            }
          );
        });
      },
    });

    // 获取 tracker 列表
    api.registerTool({
      name: "bt_get_trackers",
      description: "获取最新的 BT tracker 列表",
      inputSchema: { type: "object", properties: {} },
      handler: async () => {
        const { exec } = await import("child_process");
        return new Promise((resolve) => {
          exec(
            'curl -s https://raw.githubusercontent.com/ngosang/ngosang-trackerslist/master/trackers_best.txt | tr "\\n" "," | sed "s/,$//"',
            (err, stdout) => {
              if (err || !stdout.trim()) {
                resolve({
                  trackers: "udp://tracker.opentrackr.org:1337/announce,udp://tracker.torrent.eu.org:451/announce,udp://tracker.moeking.me:6969/announce",
                  source: "fallback",
                });
              } else {
                resolve({ trackers: stdout.trim(), source: "online" });
              }
            }
          );
        });
      },
    });

    // 检测 DHT 是否开启
    api.registerTool({
      name: "bt_check_dht",
      description: "检测 aria2 RPC 服务的 DHT (IPv4/IPv6) 状态",
      inputSchema: { type: "object", properties: {} },
      handler: async () => {
        try {
          const version = await rpcCall("aria2.getVersion");
          // DHT 状态需要通过 getGlobalOption 获取
          const options = await rpcCall("aria2.getGlobalOption");
          
          const dhtEnabled = options["enable-dht"] === "true";
          const dht6Enabled = options["enable-dht6"] === "true";
          
          return {
            dht: dhtEnabled,
            dht6: dht6Enabled,
            message: dhtEnabled ? "DHT (IPv4) 已开启" : "DHT (IPv4) 未开启",
            message6: dht6Enabled ? "DHT (IPv6) 已开启" : "DHT (IPv6) 未开启",
          };
        } catch (e: any) {
          return { error: "无法获取 DHT 状态: " + e.message, dht: false, dht6: false };
        }
      },
    });

    // 开启 DHT
    api.registerTool({
      name: "bt_enable_dht",
      description: "为 aria2 RPC 服务开启 DHT (IPv4/IPv6) 支持",
      inputSchema: {
        type: "object",
        properties: {
          dht: { type: "boolean", description: "开启 IPv4 DHT，默认 true" },
          dht6: { type: "boolean", description: "开启 IPv6 DHT，默认 true" },
        },
      },
      handler: async (args: { dht?: boolean; dht6?: boolean }) => {
        try {
          const enableDht = args.dht !== false;
          const enableDht6 = args.dht6 !== false;
          
          // 通过 aria2.changeGlobalOption 开启 DHT
          await rpcCall("aria2.changeGlobalOption", [{
            "enable-dht": enableDht ? "true" : "false",
            "enable-dht6": enableDht6 ? "true" : "false",
          }]);
          
          return {
            success: true,
            dht: enableDht,
            dht6: enableDht6,
            message: `DHT 已开启: IPv4=${enableDht}, IPv6=${enableDht6}`,
          };
        } catch (e: any) {
          return { success: false, message: "开启 DHT 失败: " + e.message };
        }
      },
    });

    // 启动 aria2 RPC 服务
    api.registerTool({
      name: "bt_start_rpc",
      description: "启动 aria2 RPC 服务（如果未启动），自动检测并开启 DHT",
      inputSchema: {
        type: "object",
        properties: {
          downloadDir: { type: "string", description: "下载保存目录" },
          seedRatio: { type: "number", description: "目标做种率（上传/下载比例），默认5" },
          seedTime: { type: "number", description: "最大做种时间（分钟），默认1440（24小时）" },
          enableDht: { type: "boolean", description: "自动开启 DHT，默认 true" },
        },
      },
      handler: async (args: { downloadDir?: string; seedRatio?: number; seedTime?: number; enableDht?: boolean }) => {
        const { exec } = await import("child_process");
        const downloadDir = args.downloadDir || process.env.DOWNLOAD_DIR || getDefaultDownloadDir();
        const seedRatio = args.seedRatio || 5;
        const seedTime = args.seedTime || 1440;
        const enableDht = args.enableDht !== false;

        return new Promise((resolve) => {
          // 检查 RPC 是否已启动
          exec("curl -s http://localhost:6800/jsonrpc -d '{\"jsonrpc\":\"2.0\",\"method\":\"aria2.getVersion\",\"id\":1}'", async (err) => {
            if (!err) {
              // RPC 已启动，检测 DHT 状态
              if (enableDht) {
                try {
                  const dhtStatus = await rpcCall("aria2.getGlobalOption");
                  const dhtEnabled = dhtStatus["enable-dht"] === "true";
                  const dht6Enabled = dhtStatus["enable-dht6"] === "true";
                  
                  if (!dhtEnabled || !dht6Enabled) {
                    await rpcCall("aria2.changeGlobalOption", [{
                      "enable-dht": "true",
                      "enable-dht6": "true",
                    }]);
                    resolve({ success: true, message: "RPC 服务已启动，DHT 已自动开启", dhtEnabled: true, dht6Enabled: true });
                    return;
                  }
                } catch (e) {
                  // 忽略 DHT 检测错误
                }
              }
              resolve({ success: true, message: "RPC 服务已启动" });
              return;
            }

            // 启动 RPC 服务，带 DHT 参数
            const dhtArgs = enableDht ? "--enable-dht --enable-dht6" : "";
            const cmd = `nohup aria2c --enable-rpc --rpc-listen-all \
              ${dhtArgs} \
              --dir="${downloadDir}" \
              --seed-ratio=${seedRatio} \
              --seed-time=${seedTime} \
              --bt-max-peers=50 \
              --bt-seed-unverified=true \
              > /tmp/aria2-rpc.log 2>&1 &`;
            
            exec(cmd, (err2) => {
              if (err2) {
                resolve({ success: false, message: "启动失败: " + err2.message });
              } else {
                // 等待服务启动
                setTimeout(() => {
                  resolve({ success: true, message: "RPC 服务已启动", dhtEnabled: enableDht, dht6Enabled: enableDht });
                }, 2000);
              }
            });
          });
        });
      },
    });

    // 执行 BT 下载（通过 RPC）
    api.registerTool({
      name: "bt_download",
      description: "使用 aria2 RPC 模式下载 BT 文件、磁力链接或普通链接",
      inputSchema: {
        type: "object",
        properties: {
          url: { type: "string", description: "下载链接、BT文件路径或磁力链接" },
          downloadDir: { type: "string", description: "保存目录（可选，不填则提示确认）" },
          useDefaultDir: { type: "boolean", description: "直接使用默认目录，跳过确认" },
          seedRatio: { type: "number", description: "目标做种率，默认5" },
          seedTime: { type: "number", description: "最大做种时间（分钟），默认1440" },
        },
        required: ["url"],
      },
      handler: async (args: { url: string; downloadDir?: string; useDefaultDir?: boolean; seedRatio?: number; seedTime?: number }) => {
        const defaultDir = process.env.DOWNLOAD_DIR || getDefaultDownloadDir();
        
        // 如果没有指定目录且用户未确认默认目录，返回确认提示
        if (!args.downloadDir && !args.useDefaultDir) {
          return {
            needConfirm: true,
            defaultDir: defaultDir,
            message: "请确认下载目录：\n1. 使用默认目录: " + defaultDir + "\n2. 指定其他目录（请回复具体路径）",
            hint: "回复「1」使用默认目录，或回复具体路径指定其他目录",
          };
        }
        
        const downloadDir = args.downloadDir || defaultDir;
        const seedRatio = args.seedRatio || 5;
        const seedTime = args.seedTime || 1440;

        // 先确保 RPC 启动
        await rpcCall("aria2.getVersion").catch(() => {
          return rpcCall("aria2.shutdown");
        }).catch(() => {});

        try {
          let result;
          if (args.url.startsWith("magnet:")) {
            result = await rpcCall("aria2.addUri", [[args.url], {
              dir: downloadDir,
              "bt-max-peers": 50,
              "seed-ratio": seedRatio,
              "seed-time": seedTime,
            }]);
          } else if (args.url.endsWith(".torrent")) {
            // 读取 torrent 文件内容
            const { readFile } = await import("fs/promises");
            const torrentContent = await readFile(args.url);
            result = await rpcCall("aria2.addTorrent", [torrentContent.toString("base64"), [], {
              dir: downloadDir,
              "bt-max-peers": 50,
              "seed-ratio": seedRatio,
              "seed-time": seedTime,
            }]);
          } else {
            result = await rpcCall("aria2.addUri", [[args.url], {
              dir: downloadDir,
              "split": 16,
              "max-connection-per-server": 16,
              "min-split-size": "10M",
            }]);
          }
          return { success: true, gid: result, message: "下载已添加" };
        } catch (e: any) {
          return { success: false, message: "添加下载失败: " + e.message };
        }
      },
    });

    // 查询做种状态
    api.registerTool({
      name: "bt_get_status",
      description: "查询当前 BT 下载/做种状态，包括做种率",
      inputSchema: { type: "object", properties: {} },
      handler: async () => {
        try {
          const globalStat = await rpcCall("aria2.getGlobalStat");
          const active = await rpcCall("aria2.tellActive");
          
          const tasks = active.map((task: any) => {
            const totalLength = parseInt(task.totalLength);
            const uploadLength = parseInt(task.uploadLength || "0");
            const completedLength = parseInt(task.completedLength);
            const seedRatio = completedLength > 0 ? (uploadLength / completedLength * 100).toFixed(1) : "0";
            const uploadSpeed = parseInt(task.uploadSpeed || "0");
            
            return {
              name: task.files?.[0]?.path?.split("/").pop() || "Unknown",
              status: task.status,
              totalSize: (totalLength / 1024 / 1024 / 1024).toFixed(2) + " GB",
              uploaded: (uploadLength / 1024 / 1024 / 1024).toFixed(2) + " GB",
              completed: (completedLength / 1024 / 1024 / 1024).toFixed(2) + " GB",
              seedRatio: seedRatio + "%",
              uploadSpeed: (uploadSpeed / 1024 / 1024).toFixed(2) + " MB/s",
              connections: task.connections,
              seeder: task.seeder,
            };
          });

          return {
            activeTasks: tasks.length,
            globalUploadSpeed: (parseInt(globalStat.uploadSpeed) / 1024 / 1024).toFixed(2) + " MB/s",
            tasks,
          };
        } catch (e: any) {
          return { error: "无法获取状态: " + e.message };
        }
      },
    });

    // 停止做种
    api.registerTool({
      name: "bt_stop_seed",
      description: "停止指定的做种任务",
      inputSchema: {
        type: "object",
        properties: {
          gid: { type: "string", description: "任务GID（可选，不填则停止所有）" },
        },
      },
      handler: async (args: { gid?: string }) => {
        try {
          if (args.gid) {
            await rpcCall("aria2.remove", [args.gid]);
            return { success: true, message: `任务 ${args.gid} 已停止` };
          } else {
            await rpcCall("aria2.pauseAll");
            return { success: true, message: "所有做种任务已暂停" };
          }
        } catch (e: any) {
          return { success: false, message: "停止失败: " + e.message };
        }
      },
    });

    // 监控做种并自动停止
    api.registerTool({
      name: "bt_monitor_and_stop",
      description: "监控做种状态，检测达到目标做种率后自动停止，并在会话中通知",
      inputSchema: {
        type: "object",
        properties: {
          targetRatio: { type: "number", description: "目标做种率（百分比），默认500%" },
        },
      },
      handler: async (args: { targetRatio?: number }) => {
        const targetRatio = args.targetRatio || 500;
        
        try {
          const active = await rpcCall("aria2.tellActive");
          const results: any[] = [];
          const stoppedTasks: string[] = [];

          for (const task of active) {
            const completedLength = parseInt(task.completedLength);
            const uploadLength = parseInt(task.uploadLength || "0");
            const currentRatio = completedLength > 0 ? (uploadLength / completedLength * 100) : 0;
            
            const fileName = task.files?.[0]?.path?.split("/").pop() || "Unknown";
            
            if (currentRatio >= targetRatio) {
              // 达到目标，停止做种
              await rpcCall("aria2.remove", [task.gid]);
              const uploadedGB = (uploadLength / 1024 / 1024 / 1024).toFixed(2);
              results.push({
                file: fileName,
                action: "已停止",
                reason: `做种率已达 ${currentRatio.toFixed(1)}%（目标 ${targetRatio}%）`,
                uploaded: uploadedGB + " GB",
              });
              stoppedTasks.push(`${fileName} (已上传 ${uploadedGB} GB)`);
            } else {
              results.push({
                file: fileName,
                action: "继续做种",
                currentRatio: currentRatio.toFixed(1) + "%",
                targetRatio: targetRatio + "%",
                uploaded: (uploadLength / 1024 / 1024 / 1024).toFixed(2) + " GB",
              });
            }
          }

          // 生成用户友好的通知消息
          let notify = "";
          if (stoppedTasks.length > 0) {
            notify = "✅ 做种任务已完成，已自动停止:\n" + stoppedTasks.map(t => "• " + t).join("\n");
          }
          
          if (results.length > stoppedTasks.length) {
            const remaining = results.length - stoppedTasks.length;
            notify += (notify ? "\n" : "") + `📊 还有 ${remaining} 个任务在继续做种`;
          }

          if (results.length === 0) {
            notify = "ℹ️ 当前没有活跃的做种任务";
          }

          return { 
            checked: results.length, 
            results,
            notify,  // 会话通知消息
            stopped: stoppedTasks.length,
          };
        } catch (e: any) {
          return { error: "监控失败: " + e.message };
        }
      },
    });

    console.log("[bt-download] 插件已加载 - 支持 RPC 模式和自动监控");
  },
};

export default plugin;
