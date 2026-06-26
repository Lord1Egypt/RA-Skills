/**
 * OpenClawGameBridge - 游戏桥接服务
 * 
 * 功能：
 * 1. 接收游戏客户端的连接注册
 * 2. 保存客户端连接（playerUid -> ws）
 * 3. 转发OpenClaw的指令到客户端
 */

const WebSocket = require('ws');
const http = require('http');

class OpenClawGameBridge {
    constructor(port = 18765) {
        this.port = port;
        this.wss = null;
        this.clients = new Map();
        this.heartbeatInterval = null;
        this.perceptions = new Map(); // 存储客户端感知数据
        this.transportPoints = new Map(); // 缓存传送门数据 mapId -> {playerUid, transportPoints}
        this.mapInfo = new Map(); // 缓存地图信息 mapId -> {mapId, mapWidth, mapHeight, gridInfo}
        this.currentMapId = null; // 当前地图ID
        this.currentMapInfo = null; // 当前地图完整信息

        this.httpServer = null;
        this.httpPort = 18766;
        this.startTime = Date.now();

        this.startServer();
        this.startHttpServer();
    }
    
    startServer() {
        this.wss = new WebSocket.Server({ port: this.port });
        
        // 心跳定时器
        this.heartbeatInterval = setInterval(() => {
            for (const [playerUid, clientWs] of this.clients) {
                if (clientWs.readyState === WebSocket.OPEN) {
                    // 发送ping保持连接
                    clientWs.ping();
                }
            }
        }, 30000); // 每30秒发送一次ping
        
        this.wss.on('connection', (ws) => {
            console.log('[Bridge] 新客户端连接');
            
            ws.isAlive = true;
            
            ws.on('pong', () => {
                ws.isAlive = true;
            });
            
            ws.on('message', (data) => {
                try {
                    const msg = JSON.parse(data);
                    console.log('[Bridge] 收到消息:', msg.type, JSON.stringify(msg).substring(0, 200));
                    this.handleMessage(msg, ws);
                } catch (error) {
                    console.error('[Bridge] 消息解析错误:', error);
                }
            });
            
            ws.on('close', () => {
                //console.log('[Bridge] 客户端断开,');
                for (const [playerUid, clientWs] of this.clients) {
                    if (clientWs === ws) {
                        this.clients.delete(playerUid);
                        console.log('[Bridge] 已移除客户端:', playerUid);
                        break;
                    }
                }
            });
            
            ws.on('error', (error) => {
                console.error('[Bridge] WebSocket错误:', error);
            });
        });
        
        this.wss.on('error', (error) => {
            console.error('[Bridge] 服务器错误:', error);
        });
        
        console.log(`[Bridge] 游戏桥接服务已启动: ws://localhost:${this.port}`);
    }
    
    handleMessage(msg, ws) {
        switch (msg.type) {
            case 'ai_register':
                this.onClientRegister(msg, ws);
                break;
                
            case 'ai_unregister':
                this.onClientUnregister(msg);
                break;
                
            case 'ai_perception':
                this.onClientPerception(msg);
                break;
                
            // AI控制端发送指令到指定玩家
            case 'ai_send_to_player':
                this.onSendToPlayer(msg);
                break;
                
            // AI控制端请求感知数据
            case 'ai_request_perception':
                this.onRequestPerception(msg);
                break;
                
            // AIController主动上报的感知数据
            case 'ai_perception_data':
                this.onPerceptionData(msg);
                break;
                
            // AIController发送的命令（包含地图信息等）
            case 'send_command':
                this.onSendCommand(msg);
                break;

            // AIController发送的地图信息（单独一个消息类型）
            case 'send_map_info':
                this.onSend_map_info(msg);
                break;

            // AI控制端请求地图信息更新
            case 'ai_request_map_update':
                this.onRequestMapUpdate(msg);
                break;

            // AIController转发的聊天消息
            case 'ai_chat_received':
                this.onChatReceived(msg);
                break;

            // 查询当前地图信息
            case 'bridge_getMapInfo':
                this.onBridgeGetMapInfo(ws, msg);
                break;

            // 查询指定地图的传送门缓存
            case 'bridge_getTransportPoints':
                this.onBridgeGetTransportPoints(ws, msg);
                break;

            // 查询所有已连接客户端
            case 'bridge_list_clients':
                this.onBridgeListClients(ws);
                break;

            // AIController发送的传送门信息
            case 'ai_transport_points':
                console.log(`[Bridge] 收到 ai_transport_points: ${JSON.stringify(msg).substring(0, 300)}`);
                this.onTransportPoints(msg);
                break;

            // 游戏客户端上报的玩家位置变化（来自 server 的 player_moved）
            case 'ai_player_moved':
                this.onPlayerMoved(msg);
                break;

            // AIController 转发的地图管理器原始数据
            case 'ai_map_manager':
                this.onMapManagerData(msg);
                break;

            // 查询缓存的地图管理器数据
            case 'bridge_getMapManagerCache':
                this.onBridgeGetMapManagerCache(ws, msg);
                break;

            // 发送控制指令到游戏客户端（移动、对话、交互等）
            case 'sendCommand':
                this.onBridgeSendCommand(ws, msg);
                break;

            // A* 查询路径
            case 'bridge_getPath':
                this.onBridgeGetPath(ws, msg);
                break;

            // 查询缓存的感知数据（按类别）
            case 'bridge_getPerception':
                this.onBridgeGetPerception(ws, msg);
                break;

            // 请求游戏客户端发送指定类别的感知数据
            case 'bridge_requestPerception':
                this.onBridgeRequestPerception(ws, msg);
                break;

            // 单项感知数据（NPCs）
            case 'ai_perception_npcs':
                this.onPerceptionNpcs(msg);
                break;

            // 单项感知数据（Players）
            case 'ai_perception_players':
                this.onPerceptionPlayers(msg);
                break;

            // 单项感知数据（Monsters）
            case 'ai_perception_monsters':
                this.onPerceptionMonsters(msg);
                break;

            // 单项感知数据（Robots）
            case 'ai_perception_robots':
                this.onPerceptionRobots(msg);
                break;

            // 单项感知数据（地图信息+传送门）
            case 'ai_perception_mapInfor':
                this.onPerceptionMapInfor(msg);
                break;

            // 单项感知数据（传送门）
            case 'ai_perception_transNodes':
                this.onPerceptionTransNodes(msg);
                break;

            // 单项感知数据（自身）
            case 'ai_perception_self':
                this.onPerceptionSelf(msg);
                break;

            // 进入地图通知（地图切换）
            case 'ai_enter_map':
                this.onEnterMap(msg);
                break;
        }
    }

    // 返回指定地图信息给请求者
    onBridgeGetMapInfo(ws, msg) {
        const mapId = msg.mapId || this.currentMapId;
        const mapInfo = mapId && this.mapInfo.has(mapId) ? this.mapInfo.get(mapId) : null;
        if (mapInfo) {
            console.log(`[Bridge] 返回地图信息: mapId=${mapInfo.mapId}`);
            ws.send(JSON.stringify({
                type: 'bridge_mapInfo',
                mapInfo: mapInfo
            }));
        } else {
            ws.send(JSON.stringify({
                type: 'bridge_mapInfo',
                mapInfo: null
            }));
            console.log(`[Bridge] 无地图信息: mapId=${mapId}`);
        }
    }

    // 返回所有已连接的客户端列表
    onBridgeListClients(ws) {
        const clientList = Array.from(this.clients.keys()).filter(k => k !== 'OPENCLAW');
        console.log(`[Bridge] 返回客户端列表:`, clientList);
        ws.send(JSON.stringify({
            type: 'bridge_clients',
            clients: clientList
        }));
    }

    // 返回指定地图的传送门缓存
    onBridgeGetTransportPoints(ws, msg) {
        const mapId = msg.mapId;
        const cached = this.transportPoints.get(mapId);
        if (cached) {
            console.log(`[Bridge] 返回传送门缓存: mapId=${mapId}, ${cached.length}个`);
            ws.send(JSON.stringify({
                type: 'bridge_transportPoints',
                mapId: mapId,
                transportPoints: cached
            }));
        } else {
            console.log(`[Bridge] 无传送门缓存: mapId=${mapId}`);
            ws.send(JSON.stringify({
                type: 'bridge_transportPoints',
                mapId: mapId,
                transportPoints: null
            }));
        }
    }

    // 发送控制指令到游戏客户端
    onBridgeSendCommand(ws, msg) {
        const playerUid = msg.playerUid;
        const command = msg.command;
        if (!playerUid || !command) {
            console.log(`[Bridge] sendCommand 缺少参数: playerUid=${playerUid}, command=`, command);
            return;
        }
        const targetWs = this.clients.get(playerUid);
        if (!targetWs || targetWs.readyState !== WebSocket.OPEN) {
            console.log(`[Bridge] sendCommand 玩家不在线: ${playerUid}`);
            return;
        }
        // 包装成 ai_control 消息发给游戏客户端
        targetWs.send(JSON.stringify({
            type: 'ai_control',
            playerUid: playerUid,
            command: command
        }));
        console.log(`[Bridge] ✅ 发送指令到 ${playerUid}:`, JSON.stringify(command));
    }

    // 返回缓存的感知数据给请求者（按类别可选）
    onBridgeGetPerception(ws, msg) {
        const playerUid = msg.playerUid || Array.from(this.clients.keys()).find(k => !k.startsWith('OPENCLAW'));
        if (!playerUid) {
            ws.send(JSON.stringify({ type: 'bridge_perception', perception: null, error: '没有已注册的玩家' }));
            return;
        }

        const cache = this.perceptionCache ? this.perceptionCache.get(playerUid) : null;
        if (!cache) {
            ws.send(JSON.stringify({ type: 'bridge_perception', playerUid, perception: null, error: '暂无感知缓存' }));
            return;
        }

        const result = {
            type: 'bridge_perception',
            playerUid: playerUid,
            perception: {
                self: cache.self,
                mapId: cache.mapId,
                position: cache.position,
                robots: Array.from(cache.robots.values()),
                players: Array.from(cache.players.values()),
                monsters: Array.from(cache.monsters.values()),
                npcs: Array.from(cache.npcs.values()),
                mapInfor: cache.mapInfor,
                transNodes: cache.transNodes
            },
            timestamp: Date.now()
        };
        ws.send(JSON.stringify(result));
        console.log(`[Bridge] 返回感知缓存: playerUid=${playerUid}, robots=${cache.robots.size}, npcs=${cache.npcs.size}`);
    }

    // 请求游戏客户端发送指定类别的感知数据
    onBridgeRequestPerception(ws, msg) {
        const playerUid = msg.playerUid || Array.from(this.clients.keys()).find(k => !k.startsWith('OPENCLAW'));
        const category = msg.category; // 'robots', 'npcs', 'monsters', 'players', 'mapInfor', 'transNodes', 'all'

        if (!playerUid) {
            ws.send(JSON.stringify({ type: 'bridge_perception_response', error: '没有已注册的玩家' }));
            return;
        }

        const targetWs = this.clients.get(playerUid);
        if (!targetWs || targetWs.readyState !== WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: 'bridge_perception_response', error: `玩家 ${playerUid} 不在线` }));
            return;
        }

        if (category === 'all' || !category) {
            // 请求完整感知数据
            targetWs.send(JSON.stringify({
                type: 'ai_control',
                command: { type: 'get_perception' }
            }));
            console.log(`[Bridge] 请求完整感知数据 from ${playerUid}`);
        } else {
            // 请求单项感知，映射到对应的 AIController 方法
            const singlePerceptionMap = {
                'robots': 'getPerception_robots_toBridge',
                'monsters': 'getPerception_monsters_toBridge',
                'npcs': 'getPerception_npcs_toBridge',
                'players': 'getPerception_players_toBridge',
                'mapInfor': 'getPerception_mapInfor_toBridge',
                'transNodes': 'getPerception_transNodes_toBridge',
                'self': 'getPerception_self_toBridge'
            };
            const methodName = singlePerceptionMap[category];
            if (methodName) {
                targetWs.send(JSON.stringify({
                    type: 'ai_control',
                    command: { type: methodName }
                }));
                console.log(`[Bridge] 请求单项感知 from ${playerUid}, category=${category}, method=${methodName}`);
            } else {
                console.log(`[Bridge] 未知 category: ${category}，发送完整感知`);
                targetWs.send(JSON.stringify({
                    type: 'ai_control',
                    command: { type: 'get_perception' }
                }));
            }
        }

        ws.send(JSON.stringify({ type: 'bridge_perception_response', status: '请求已发送', playerUid, category }));
    }

    // ==================== 单项感知数据处理 ====================

    // 单项感知：NPCs
    onPerceptionNpcs(msg) {
        if (!this.perceptionCache || !this.perceptionCache.has(msg.playerUid)) {
            this.initPlayerPerceptionCache(msg.playerUid);
        }
        const cache = this.perceptionCache.get(msg.playerUid);
        if (msg.npcs) {
            cache.npcs.clear();
            for (const n of msg.npcs) {
                if (n.npcId) cache.npcs.set(n.npcId, n);
            }
        }
        this.broadcastToOpenClaw({
            type: 'ai_perception_npcs',
            playerUid: msg.playerUid,
            npcs: msg.npcs
        });
        console.log(`[Bridge] 单项感知缓存已更新: npcs, count=${msg.npcs?.length || 0}`);
    }

    // 单项感知：Players
    onPerceptionPlayers(msg) {
        if (!this.perceptionCache || !this.perceptionCache.has(msg.playerUid)) {
            this.initPlayerPerceptionCache(msg.playerUid);
        }
        const cache = this.perceptionCache.get(msg.playerUid);
        if (msg.players) {
            cache.players.clear();
            for (const p of msg.players) {
                if (p.playerUid) cache.players.set(p.playerUid, p);
            }
        }
        this.broadcastToOpenClaw({
            type: 'ai_perception_players',
            playerUid: msg.playerUid,
            players: msg.players
        });
        console.log(`[Bridge] 单项感知缓存已更新: players, count=${msg.players?.length || 0}`);
    }

    // 单项感知：Monsters
    onPerceptionMonsters(msg) {
        if (!this.perceptionCache || !this.perceptionCache.has(msg.playerUid)) {
            this.initPlayerPerceptionCache(msg.playerUid);
        }
        const cache = this.perceptionCache.get(msg.playerUid);
        if (msg.monsters) {
            cache.monsters.clear();
            for (const m of msg.monsters) {
                if (m.Uid) cache.monsters.set(m.Uid, m);
            }
        }
        this.broadcastToOpenClaw({
            type: 'ai_perception_monsters',
            playerUid: msg.playerUid,
            monsters: msg.monsters
        });
        console.log(`[Bridge] 单项感知缓存已更新: monsters, count=${msg.monsters?.length || 0}`);
    }

    // 单项感知：Robots
    onPerceptionRobots(msg) {
        if (!this.perceptionCache || !this.perceptionCache.has(msg.playerUid)) {
            this.initPlayerPerceptionCache(msg.playerUid);
        }
        const cache = this.perceptionCache.get(msg.playerUid);
        if (msg.robots) {
            cache.robots.clear();
            for (const r of msg.robots) {
                if (r.playerUid) cache.robots.set(r.playerUid, r);
            }
        }
        this.broadcastToOpenClaw({
            type: 'ai_perception_robots',
            playerUid: msg.playerUid,
            robots: msg.robots
        });
        console.log(`[Bridge] 单项感知缓存已更新: robots, count=${msg.robots?.length || 0}`);
    }

    // 单项感知：地图信息（含传送门）
    onPerceptionMapInfor(msg) {
        if (!this.perceptionCache || !this.perceptionCache.has(msg.playerUid)) {
            this.initPlayerPerceptionCache(msg.playerUid);
        }
        const cache = this.perceptionCache.get(msg.playerUid);
        cache.mapInfor = msg.mapInfor || null;
        if (msg.transNodes) {
            cache.transNodes = msg.transNodes;
        }
        // 同时更新 mapInfo 缓存
        if (msg.mapInfor?.map_id) {
            this.mapInfo.set(msg.mapInfor.map_id, {
                mapId: msg.mapInfor.map_id,
                mapWidth: msg.mapInfor.map_width,
                mapHeight: msg.mapInfor.map_height,
                gridInfo: msg.mapInfor.grid_info
            });
            this.currentMapId = msg.mapInfor.map_id;
            this.currentMapInfo = this.mapInfo.get(msg.mapInfor.map_id);
        }
        this.broadcastToOpenClaw({
            type: 'ai_perception_mapInfor',
            playerUid: msg.playerUid,
            mapInfor: msg.mapInfor,
            transNodes: msg.transNodes
        });
        console.log(`[Bridge] 单项感知缓存已更新: mapInfor mapId=${msg.mapInfor?.map_id}`);
    }

    // 单项感知：传送门
    onPerceptionTransNodes(msg) {
        if (!this.perceptionCache || !this.perceptionCache.has(msg.playerUid)) {
            this.initPlayerPerceptionCache(msg.playerUid);
        }
        const cache = this.perceptionCache.get(msg.playerUid);
        cache.transNodes = msg.transNodes || [];
        // 缓存传送门数据
        if (msg.playerUid && msg.transNodes) {
            this.transportPoints.set(this.currentMapId || msg.playerUid, msg.transNodes);
        }
        this.broadcastToOpenClaw({
            type: 'ai_perception_transNodes',
            playerUid: msg.playerUid,
            transNodes: msg.transNodes
        });
        console.log(`[Bridge] 单项感知缓存已更新: transNodes, count=${msg.transNodes?.length || 0}`);
    }

    // 单项感知：自身数据
    onPerceptionSelf(msg) {
        if (!this.perceptionCache || !this.perceptionCache.has(msg.playerUid)) {
            this.initPlayerPerceptionCache(msg.playerUid);
        }
        const cache = this.perceptionCache.get(msg.playerUid);
        cache.self = msg.self || null;
        cache.position = msg.position || null;
        this.broadcastToOpenClaw({
            type: 'ai_perception_self',
            playerUid: msg.playerUid,
            self: msg.self,
            position: msg.position
        });
        console.log(`[Bridge] 单项感知缓存已更新: self`);
    }

    // 进入地图通知（由 AIController.enterMap 触发）
    onEnterMap(msg) {
        const playerUid = msg.playerUid;
        const newMapId = msg.mapId;
        console.log(`[Bridge] 收到 ai_enter_map: playerUid=${playerUid}, mapId=${newMapId}`);

        if (!this.perceptionCache || !this.perceptionCache.has(playerUid)) {
            this.initPlayerPerceptionCache(playerUid);
        }
        const cache = this.perceptionCache.get(playerUid);

        // 清空旧地图实体缓存
        cache.robots.clear();
        cache.players.clear();
        cache.monsters.clear();
        cache.npcs.clear();
        cache.mapInfor = null;
        cache.transNodes = [];

        // 更新当前地图ID
        cache.mapId = newMapId;
        this.currentMapId = newMapId;

        // 广播地图切换给 OPENCLAW 客户端
        this.broadcastToOpenClaw({
            type: 'ai_map_changed',
            playerUid: playerUid,
            mapId: newMapId
        });

        // 向游戏客户端请求完整感知数据
        const targetWs = this.clients.get(playerUid);
        if (targetWs && targetWs.readyState === WebSocket.OPEN) {
            setTimeout(() => {
                targetWs.send(JSON.stringify({
                    type: 'ai_control',
                    command: { type: 'get_perception' }
                }));
                console.log(`[Bridge] ai_enter_map 已发送 get_perception 请求到 ${playerUid}`);
            }, 1000);
        }
    }

    // 处理聊天消息（转发给OpenClaw控制端）
    onChatReceived(msg) {
        console.log(`[Bridge] 收到聊天消息: playerUid=${msg.playerUid}, chat=`, msg.chat);
        this.broadcastToOpenClaw({
            type: 'ai_chat_received',
            playerUid: msg.playerUid,
            chat: msg.chat
        });
    }

    // 处理游戏客户端上报的玩家位置变化
    onPlayerMoved(msg) {
        console.log(`[Bridge] 收到位置更新: playerUid=${msg.playerUid}, position=${JSON.stringify(msg.position)}`);
        this.broadcastToOpenClaw({
            type: 'ai_player_moved',
            playerUid: msg.playerUid,
            position: msg.position
        });
    }

    // 处理 AIController 转发的地图管理器数据（玩家进出、机器人/NPC/怪物状态等）
    onMapManagerData(msg) {
        console.log(`[Bridge] 收到 ai_map_manager: playerUid=${msg.playerUid}, subType=${msg.mapManagerData?.subType}, 原始数据=`, JSON.stringify(msg.mapManagerData).substring(0, 300));
        const data = msg.mapManagerData;

        // 初始化分类缓存（按实体UID存取，与RobotLoad一致）
        if (!this.mapManagerCache) {
            this.mapManagerCache = {
                robots: new Map(),       // playerUid -> robotData
                players: new Map(),       // playerUid -> playerData
                monsters: new Map(),      // monsterUid -> monsterData
                npcs: new Map(),          // npcId -> npcData
                pets: new Map(),          // petUid -> petData
                chests: new Map(),        // chestId -> chestData
                shops: new Map()          // shopId -> shopData
            };
        }

        const cache = this.mapManagerCache;

        switch (data.subType) {
            case 'creatRobot':
                if (data.robot?.playerUid) {
                    cache.robots.set(data.robot.playerUid, data.robot);
                }
                break;

            case 'creatRobots':  // 批量创建
                if (Array.isArray(data.robots)) {
                    for (const robot of data.robots) {
                        if (robot.playerUid) cache.robots.set(robot.playerUid, robot);
                    }
                }
                break;

            case 'removeRobot':
                if (data.playerUid) {
                    cache.robots.delete(data.playerUid);
                }
                break;

            case 'robot_moved':
                if (data.robot?.playerUid) {
                    // 已有则更新位置，无则创建一条
                    const existing = cache.robots.get(data.robot.playerUid);
                    cache.robots.set(data.robot.playerUid, existing ? { ...existing, ...data.robot } : data.robot);
                }
                break;

            case 'creatMonserTeam':
                if (data.monsterTeam?.Uid) {
                    cache.monsters.set(data.monsterTeam.Uid, data.monsterTeam);
                }
                break;

            case 'creatMonserTeams':  // 批量创建
                if (Array.isArray(data.monsterTeams)) {
                    for (const m of data.monsterTeams) {
                        if (m.Uid) cache.monsters.set(m.Uid, m);
                    }
                }
                break;

            case 'removeMonsterTeam':
                if (data.monsterUid) {
                    cache.monsters.delete(data.monsterUid);
                }
                break;

            case 'monster_moved':
                if (data.monsterTeam?.Uid) {
                    const existing = cache.monsters.get(data.monsterTeam.Uid);
                    cache.monsters.set(data.monsterTeam.Uid, existing ? { ...existing, ...data.monsterTeam } : data.monsterTeam);
                }
                break;

            case 'monsterChangeStatus':
                if (data.monsterUid) {
                    const existing = cache.monsters.get(data.monsterUid);
                    cache.monsters.set(data.monsterUid, existing ? { ...existing, status: data.status } : { Uid: data.monsterUid, status: data.status });
                }
                break;

            case 'creatNPCs':  // 批量创建
                if (Array.isArray(data.npcs)) {
                    for (const npc of data.npcs) {
                        if (npc.npcId) cache.npcs.set(npc.npcId, npc);
                    }
                }
                break;

            case 'mapNodes':
                // 完整地图数据，覆盖更新所有玩家
                if (data.players) {
                    cache.players.clear();
                    for (const uid in data.players) {
                        cache.players.set(uid, data.players[uid]);
                    }
                }
                // 保存 self 信息（玩家自己的位置）
                if (data.mapId) {
                    const isMapChange = cache.currentMapId !== null && cache.currentMapId !== data.mapId;
                    cache.currentMapId = data.mapId;
                    // 如果 mapId 变化（从 mapChanged 之外的路径触发），主动请求感知数据
                    if (isMapChange) {
                        cache.robots.clear();
                        cache.players.clear();
                        cache.monsters.clear();
                        cache.npcs.clear();
                        this.broadcastToOpenClaw({
                            type: 'ai_map_changed',
                            playerUid: msg.playerUid,
                            mapId: data.mapId
                        });
                        console.log(`[Bridge] mapNodes 检测到地图切换: ${cache.currentMapId} -> ${data.mapId}，缓存已清空`);
                        const targetWs = this.clients.get(msg.playerUid);
                        if (targetWs && targetWs.readyState === WebSocket.OPEN) {
                            setTimeout(() => {
                                targetWs.send(JSON.stringify({
                                    type: 'ai_control',
                                    command: { type: 'get_perception' }
                                }));
                                console.log(`[Bridge] mapNodes 切换，已发送 get_perception 请求到 ${msg.playerUid}`);
                            }, 1000);
                        }
                    }
                }
                break;

            case 'mapChanged':
                // 地图切换，清空旧地图的实体缓存，缓存新地图ID
                console.log(`[Bridge] 收到 mapChanged: playerUid=${msg.playerUid}, data=`, JSON.stringify(data).substring(0, 300));
                if (data.mapId) {
                    cache.currentMapId = data.mapId;
                    cache.robots.clear();
                    cache.players.clear();
                    cache.monsters.clear();
                    cache.npcs.clear();
                    cache.mapInfor = null;
                    cache.transNodes = [];
                    this.broadcastToOpenClaw({
                        type: 'ai_map_changed',
                        playerUid: msg.playerUid,
                        mapId: data.mapId
                    });
                    console.log(`[Bridge] 地图切换: playerUid=${msg.playerUid} -> mapId=${data.mapId}，缓存已清空`);

                    // 主动请求游戏客户端发送完整感知数据
                    const targetWs = this.clients.get(msg.playerUid);
                    if (targetWs && targetWs.readyState === WebSocket.OPEN) {
                        setTimeout(() => {
                            targetWs.send(JSON.stringify({
                                type: 'ai_control',
                                command: { type: 'get_perception' }
                            }));
                            console.log(`[Bridge] 地图切换，已发送 get_perception 请求到 ${msg.playerUid}`);
                        }, 1000); // 等待1秒让游戏客户端加载完地图节点
                    }
                }
                break;

            case 'player_joinMap':
                if (data.player && data.playerUid) {
                    cache.players.set(data.playerUid, data.player);
                }
                break;

            case 'player_levelMap':
                if (data.playerUid) {
                    cache.players.delete(data.playerUid);
                }
                break;
        }

        // 广播给所有OPENCLAW客户端
        this.broadcastToOpenClaw({
            type: 'ai_map_manager',
            playerUid: msg.playerUid,
            mapManagerData: data,
            cacheVersion: Date.now()  // 通知客户端缓存有更新
        });
    }

    // 返回缓存的地图管理器数据
    onBridgeGetMapManagerCache(ws, msg) {
        const cache = this.mapManagerCache;
        if (!cache) {
            ws.send(JSON.stringify({ type: 'bridge_mapManagerCache', cache: null }));
            return;
        }
        // 收集所有地图的传送门
        const allTransportPoints = [];
        for (const [mapId, tps] of this.transportPoints.entries()) {
            for (const tp of tps) {
                allTransportPoints.push({ mapId, ...tp });
            }
        }

        const result = {
            type: 'bridge_mapManagerCache',
            robots: Array.from(cache.robots?.values() || []),
            players: Array.from(cache.players?.values() || []),
            monsters: Array.from(cache.monsters?.values() || []),
            npcs: Array.from(cache.npcs?.values() || []),
            transportPoints: allTransportPoints,
            timestamp: Date.now()
        };
        ws.send(JSON.stringify(result));
    }

    // 通用广播方法：发送给所有OPENCLAW客户端
    broadcastToOpenClaw(msg) {
        for (const [id, clientWs] of this.clients) {
            if (id.startsWith('OPENCLAW') && clientWs.readyState === WebSocket.OPEN) {
                clientWs.send(JSON.stringify(msg));
            }
        }
    }

    // 处理传送门信息（缓存并转发给OpenClaw控制端）
    onTransportPoints(msg) {
        console.log(`[Bridge] 收到传送门信息: mapId=${msg.currentMapId}, ${msg.transportPoints?.length}个`);
        
        // 缓存传送门数据（按地图ID累加存放）
        const existing = this.transportPoints.get(msg.currentMapId) || [];
        const existingKeys = new Set(existing.map(t => t.gridX + '#' + t.gridY));
        for (const tp of msg.transportPoints) {
            const key = tp.gridX + '#' + tp.gridY;
            if (!existingKeys.has(key)) {
                existing.push(tp);
                existingKeys.add(key);
            }
        }
        this.transportPoints.set(msg.currentMapId, existing);
        console.log(`[Bridge] 传送门数据已缓存: mapId=${msg.currentMapId}, 累计${existing.length}个`);
        
        // 广播给所有OPENCLAW客户端
        this.broadcastToOpenClaw({
            type: 'ai_transport_points',
            playerUid: msg.playerUid,
            currentMapId: msg.currentMapId,
            transportPoints: msg.transportPoints
        });
        console.log(`[Bridge] 传送门信息已广播`);
    }
    
    // 处理命令消息（来自AIController）
    onSendCommand(msg) {
        const playerUid = msg.player_uid;
        const mapInfor = msg.mapInfor;
        
        if (!mapInfor) return;
        
        if (mapInfor.cmd === 'map_info') {
            // 存储地图信息
            this.mapInfo.set(mapInfor.map_id, {
                mapId: mapInfor.map_id,
                mapWidth: mapInfor.map_width,
                mapHeight: mapInfor.map_height,
                gridInfo: mapInfor.grid_info
            });
            // 设置为当前地图
            this.currentMapInfo = this.mapInfo.get(mapInfor.map_id);
            console.log(`[Bridge] 收到地图信息: mapId=${mapInfor.map_id}, size=${mapInfor.map_width}x${mapInfor.map_height}`);
        }
    }
    
    // 处理地图信息（来自AIController，单独消息类型）
    onSend_map_info(msg) {
        const playerUid = msg.player_uid;
        const mapInfor = msg.mapInfor;
        
        if (!mapInfor) return;
        console.log(`[Bridge] 收到地图信息: mapId=${mapInfor.map_id}, cmd=${mapInfor.cmd}`,this.currentMapId,mapInfor.map_id);
        // 只有 cmd === 'map_info' 才是真正的地图信息，其他是事件转发
        //if (mapInfor.cmd !== 'map_info') return;

        // 只在 mapId 变化时更新
        if (this.currentMapId !== mapInfor.map_id || this.currentMapId === null) {
            const oldMapId = this.currentMapId;
            this.currentMapId = mapInfor.map_id;
            this.mapInfo.set(mapInfor.map_id, {
                mapId: mapInfor.map_id,
                mapWidth: mapInfor.map_width,
                mapHeight: mapInfor.map_height,
                gridInfo: mapInfor.grid_info
            });
            this.currentMapInfo = this.mapInfo.get(mapInfor.map_id);
            console.log(`[Bridge] 地图切换: mapId=${oldMapId} -> ${mapInfor.map_id}, size=${mapInfor.map_width}x${mapInfor.map_height}`);

            // 清空旧地图的实体缓存（新地图数据等 get_perception 返回后更新）
            if (this.perceptionCache && this.perceptionCache.has(playerUid)) {
                const cache = this.perceptionCache.get(playerUid);
                cache.robots.clear();
                cache.players.clear();
                cache.monsters.clear();
                cache.npcs.clear();
                cache.mapInfor = null;
                cache.transNodes = [];
                cache.mapId = mapInfor.map_id;
            }

            // 通知所有 OPENCLAW 客户端地图已切换
            this.broadcastToOpenClaw({
                type: 'ai_map_changed',
                playerUid: playerUid,
                mapId: mapInfor.map_id,
                mapWidth: mapInfor.map_width,
                mapHeight: mapInfor.map_height
            });

            // 地图切换后，主动请求游戏客户端发送完整感知数据
            const targetWs = this.clients.get(playerUid);
            if (targetWs && targetWs.readyState === WebSocket.OPEN) {
                setTimeout(() => {
                    targetWs.send(JSON.stringify({
                        type: 'ai_control',
                        command: { type: 'get_perception' }
                    }));
                    console.log(`[Bridge] 地图切换，已发送 get_perception 请求到 ${playerUid}`);
                }, 1000); // 等待1秒让游戏客户端加载完地图节点
            }
        }
    }

    // AI控制端请求地图信息更新
    onRequestMapUpdate(msg) {
        const playerUid = msg.playerUid;
        const targetWs = this.clients.get(playerUid);
        if (targetWs && targetWs.readyState === WebSocket.OPEN) {
            targetWs.send(JSON.stringify({ type: 'ai_request_map_update' }));
            console.log(`[Bridge] 请求 ${playerUid} 更新地图信息`);
        }
    }
    
    // 检查坐标是否可通行
    isWalkable(mapId, x, y) {
        const map = this.mapInfo.has(mapId) ? this.mapInfo.get(mapId) : null;
        console.log(`[Bridge] isWalkable mapId=${mapId} map=${map?'有':'无'} gridInfo=${map?.gridInfo?'有':'无'} mapId字段=${map?.mapId}`);
        if (!map || !map.gridInfo) return true; // 无数据默认可通行
        
        const grid = map.gridInfo;
        if (x < 0 || x >= map.mapWidth || y < 0 || y >= map.mapHeight) return false;
        
        // gridInfo格式：[x][y] = true可通行，false障碍
        const val = (grid[x] && grid[x][y] !== undefined) ? grid[x][y] : 'undefined';
        console.log(`[Bridge] isWalkable(${mapId},${x},${y}) val=${val} grid[${x}][${y}]=${grid[x]?.[y]}`);
        if (grid[x] && grid[x][y] !== undefined) {
            return grid[x][y] === true;
        }
        return true;
    }
    
    // 查找距离指定坐标最近的可行走位置
    findNearestWalkable(x, y, map) {
        const range = 5;
        for (let d = 1; d <= range; d++) {
            for (let dx = -d; dx <= d; dx++) {
                for (let dy = -d; dy <= d; dy++) {
                    const nx = x + dx;
                    const ny = y + dy;
                    if (this.isWalkable(map.mapId, nx, ny)) {
                        return { x: nx, y: ny };
                    }
                }
            }
        }
        return null;
    }
    
    // AI控制端发送指令到指定玩家
    onSendToPlayer(msg) {
        const targetPlayerUid = msg.targetPlayerUid;
        const command = msg.command;
        
        // 如果是移动指令，检查目标是否可通行
        if (command.type === 'move' && this.currentMapInfo) {
            const x = Math.round(command.x);
            const y = Math.round(command.y);
            console.log(`[Bridge] 移动检查: currentMapInfo.mapId=${this.currentMapInfo.mapId}, target=${x},${y}`);
            
            if (!this.isWalkable(this.currentMapInfo.mapId, x, y)) {
                console.log(`[Bridge] 目标 ${x},${y} 不可通行，查找最近可行走位置`);
                const nearest = this.findNearestWalkable(x, y, this.currentMapInfo);
                if (nearest) {
                    console.log(`[Bridge] 已调整为最近可行走位置: ${nearest.x},${nearest.y}`);
                    command.x = nearest.x;
                    command.y = nearest.y;
                } else {
                    console.warn(`[Bridge] 附近无可行走位置`);
                    return; // 不发送不可通行的移动
                }
            }
        }
        
        const targetWs = this.clients.get(targetPlayerUid);
        if (targetWs && targetWs.readyState === WebSocket.OPEN) {
            targetWs.send(JSON.stringify({
                type: 'ai_control',
                command: command
            }));
            console.log(`[Bridge] ✅ 转发指令到 ${targetPlayerUid}:`, command);
        } else {
            console.warn(`[Bridge] ❌ 玩家 ${targetPlayerUid} 不在线或连接无效`);
        }
    }
    
    onClientRegister(msg, ws) {
        // 处理空的playerUid
        let playerUid = msg.playerUid;
        if (!playerUid || playerUid === '') {
            playerUid = 'player_001';
            console.log(`[Bridge] ⚠️ 玩家ID为空，已自动设置为: player_001`);
        }
        
        this.clients.set(playerUid, ws);
        console.log(`[Bridge] ⭐ 客户端注册: playerUid=${playerUid}, ws=${ws.readyState}`);
        console.log(`[Bridge] 当前保存的客户端:`, Array.from(this.clients.keys()));
        
        ws.send(JSON.stringify({
            type: 'ai_registered',
            playerUid: playerUid,
            status: 'ok'
        }));
        
        // 如果是游戏客户端注册，通知OpenClaw
        // 检查是否有OpenClaw控制端连接
        const openClawClient = this.clients.get('OPENCLAW');
        if (openClawClient && openClawClient.readyState === WebSocket.OPEN) {
            openClawClient.send(JSON.stringify({
                type: 'ai_client_connected',
                playerUid: playerUid
            }));
        }

        // 初始化该玩家的感知缓存
        this.initPlayerPerceptionCache(playerUid);

        // 主动请求游戏客户端发送完整感知数据
        setTimeout(() => {
            if (ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({
                    type: 'ai_control',
                    command: { type: 'get_perception' }
                }));
                console.log(`[Bridge] 客户端注册完成，已发送 get_perception 请求到 ${playerUid}`);
            }
        }, 500);

        console.log(`[Bridge] 已通知OpenClaw：玩家 ${playerUid} 已准备好`);
    }

    // 初始化玩家的感知缓存结构
    initPlayerPerceptionCache(playerUid) {
        if (!this.perceptionCache) {
            this.perceptionCache = new Map();
        }
        this.perceptionCache.set(playerUid, {
            self: null,
            mapId: null,
            position: null,
            robots: new Map(),
            players: new Map(),
            monsters: new Map(),
            npcs: new Map(),
            mapInfor: null,
            transNodes: []
        });
        console.log(`[Bridge] 感知缓存已初始化: playerUid=${playerUid}`);
    }

    // 更新感知缓存（从 ai_perception_data 的完整数据中更新）
    updatePerceptionCache(playerUid, p) {
        console.log(`[Bridge] 感知缓存更新: playerUid=${playerUid}, robots=${p.robots?.length ?? 'Map'}, monsters=${p.monsters?.length ?? 'Map'}`);
        if (!this.perceptionCache || !this.perceptionCache.has(playerUid)) {
            this.initPlayerPerceptionCache(playerUid);
        }
        const cache = this.perceptionCache.get(playerUid);

        // self
        if (p.self !== undefined) {
            cache.self = p.self;
        }
        // mapId
        if (p.mapId !== undefined) {
            cache.mapId = p.mapId;
        }
        // position
        if (p.position !== undefined) {
            cache.position = p.position;
        }
        // robots
        if (p.robots !== undefined) {
            cache.robots.clear();
            if (Array.isArray(p.robots)) {
                for (const r of p.robots) {
                    if (r.playerUid) cache.robots.set(r.playerUid, r);
                }
            } else if (p.robots instanceof Map) {
                // Map 格式：{ playerUid -> robotData }
                for (const [uid, robotData] of p.robots) {
                    cache.robots.set(uid, robotData);
                }
            }
            console.log(`[Bridge] robots缓存已更新: size=${cache.robots.size}, 来源=${Array.isArray(p.robots) ? 'array' : 'Map'}`);
        }
        // players
        if (p.players !== undefined) {
            cache.players.clear();
            if (Array.isArray(p.players)) {
                for (const pl of p.players) {
                    if (pl.playerUid) cache.players.set(pl.playerUid, pl);
                }
            } else if (p.players instanceof Map) {
                for (const [uid, playerData] of p.players) {
                    cache.players.set(uid, playerData);
                }
            }
        }
        // monsters
        if (p.monsters !== undefined) {
            cache.monsters.clear();
            if (Array.isArray(p.monsters)) {
                for (const m of p.monsters) {
                    // 支持大写 Uid 或小写 uid
                    const key = m.Uid || m.uid;
                    if (key) cache.monsters.set(key, m);
                }
            } else if (p.monsters instanceof Map) {
                for (const [uid, monsterData] of p.monsters) {
                    cache.monsters.set(uid, monsterData);
                }
            }
            console.log(`[Bridge] 感知缓存已更新: playerUid=${playerUid}, monsters=${cache.monsters.size}, 示例=${JSON.stringify(p.monsters?.[0])}`);
        }
        // npcs
        if (p.npcs !== undefined) {
            cache.npcs.clear();
            if (Array.isArray(p.npcs)) {
                for (const n of p.npcs) {
                    if (n.npcId) cache.npcs.set(n.npcId, n);
                }
            } else if (p.npcs instanceof Map) {
                for (const [npcId, npcData] of p.npcs) {
                    cache.npcs.set(npcId, npcData);
                }
            }
        }
        // mapInfor
        if (p.mapInfor !== undefined) {
            cache.mapInfor = p.mapInfor;
        }
        // transNodes
        if (p.transNodes !== undefined) {
            cache.transNodes = Array.isArray(p.transNodes) ? p.transNodes : [];
        }

        console.log(`[Bridge] 感知缓存已更新: playerUid=${playerUid}, robots=${cache.robots.size}, players=${cache.players.size}, monsters=${cache.monsters.size}, npcs=${cache.npcs.size}`,cache.mapInfor);
    }
    
    onClientUnregister(msg) {
        const playerUid = msg.playerUid;
        if (this.clients.has(playerUid)) {
            this.clients.delete(playerUid);
            console.log(`[Bridge] 客户端取消注册: ${playerUid}`);
        }
    }
    
    onClientPerception(msg) {
        console.log(`[Bridge] 收到感知数据: ${msg.playerUid}`);
        // 存储感知数据
        if (msg.perception) {
            this.perceptions.set(msg.playerUid, msg.perception);
        }
        
        // 转发感知数据给OpenClaw控制端
        const openClawClient = this.clients.get('OPENCLAW');
        if (openClawClient && openClawClient.readyState === WebSocket.OPEN) {
            openClawClient.send(JSON.stringify({
                type: 'ai_perception_update',
                playerUid: msg.playerUid,
                perception: msg.perception
            }));
        }
    }
    
    // 处理感知数据（来自AIController的主动上报）
    onPerceptionData(msg) {


        const p = msg.perception;
        console.log(`[Bridge] 收到AIController感知数据: playerUid=${msg.playerUid}`,p);
        if (!p) {
            console.log(`[Bridge] 感知数据为空，忽略`);
            return;
        }

        // 更新结构化感知缓存
        this.updatePerceptionCache(msg.playerUid, p);

        // 转发给OpenClaw控制端（使用缓存确保数据完整）
        const cache = this.perceptionCache ? this.perceptionCache.get(msg.playerUid) : null;
        const toArray = (m) => {
            if (!m) return [];
            if (m instanceof Map) return Array.from(m.values());
            if (Array.isArray(m)) return m;
            if (typeof m === 'object') return Object.values(m);
            return [];
        };

        // 发送给所有OPENCLAW开头的客户端
        let sent = false;
        for (const [id, clientWs] of this.clients) {
            if (id.startsWith('OPENCLAW') && clientWs.readyState === WebSocket.OPEN) {
                clientWs.send(JSON.stringify({
                    type: 'ai_perception_data',
                    playerUid: msg.playerUid,
                    perception: {
                        self: cache?.self || p.self || null,
                        position: cache?.position || p.position || null,
                        mapId: cache?.mapId || p.mapId || null,
                        robots: cache ? Array.from(cache.robots.values()) : toArray(p.robots),
                        npcs: cache ? Array.from(cache.npcs.values()) : toArray(p.npcs),
                        monsters: cache ? Array.from(cache.monsters.values()) : toArray(p.monsters),
                        players: cache ? Array.from(cache.players.values()) : toArray(p.players),
                        mapInfor: cache?.mapInfor || p.mapInfor || null,
                        transNodes: cache?.transNodes || [],
                        _cacheVersion: Date.now()
                    }
                }));
                console.log(`[Bridge] 感知数据已发送给 ${id}`);
                sent = true;
            }
        }
        if (!sent) console.log(`[Bridge] 没有在线的OPENCLAW客户端`);
    }

    // AI控制端请求感知数据（通过桥接缓存）
    onRequestPerception(msg) {
        const targetPlayerUid = msg.targetPlayerUid;
        const cache = this.perceptionCache ? this.perceptionCache.get(targetPlayerUid) : null;

        if (!cache) {
            console.log(`[Bridge] perceptionCache 为空，请先进入地图或等待客户端发送感知数据`);
            return;
        }

        // 从缓存组装感知数据，直接返回给 OPENCLAW 客户端
        const openClawClient = this.clients.get('OPENCLAW');
        if (!openClawClient || openClawClient.readyState !== WebSocket.OPEN) {
            for (const [id, clientWs] of this.clients) {
                if (id.startsWith('OPENCLAW') && clientWs.readyState === WebSocket.OPEN) {
                    clientWs.send(JSON.stringify({
                        type: 'ai_perception_data',
                        playerUid: targetPlayerUid,
                        perception: {
                            self: cache.self,
                            position: cache.position,
                            mapId: cache.mapId,
                            robots: Array.from(cache.robots.values()),
                            players: Array.from(cache.players.values()),
                            monsters: Array.from(cache.monsters.values()),
                            npcs: Array.from(cache.npcs.values()),
                            mapInfor: cache.mapInfor,
                            transNodes: cache.transNodes
                        }
                    }));
                    console.log(`[Bridge] 感知数据已从缓存返回给 ${id}`);
                    break;
                }
            }
            return;
        }

        openClawClient.send(JSON.stringify({
            type: 'ai_perception_data',
            playerUid: targetPlayerUid,
            perception: {
                self: cache.self,
                position: cache.position,
                mapId: cache.mapId,
                robots: Array.from(cache.robots.values()),
                players: Array.from(cache.players.values()),
                monsters: Array.from(cache.monsters.values()),
                npcs: Array.from(cache.npcs.values()),
                mapInfor: cache.mapInfor,
                transNodes: cache.transNodes
            }
        }));
        console.log(`[Bridge] 感知数据已从缓存返回`);
    }

    setAIMode(playerUid, enabled) {
        const ws = this.clients.get(playerUid);
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({
                type: 'ai_set_mode',
                enabled: enabled
            }));
            console.log(`[Bridge] 发送模式设置: ${playerUid} -> ${enabled}`);
            return true;
        } else {
            console.warn(`[Bridge] 玩家不在线: ${playerUid}`);
            return false;
        }
    }
    
    sendCommand(playerUid, command) {
        console.log(`[Bridge] ⭐ 尝试发送指令到 ${playerUid}`);
        console.log(`[Bridge] 当前保存的客户端:`, Array.from(this.clients.keys()));
        
        const ws = this.clients.get(playerUid);
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({
                type: 'ai_control',
                command: command
            }));
            console.log(`[Bridge] ✅ 发送指令成功到 ${playerUid}:`, command);
            return true;
        } else {
            console.warn(`[Bridge] ❌ 玩家不在线或ws无效: ${playerUid}, ws=${ws ? ws.readyState : 'undefined'}`);
            return false;
        }
    }
    
    requestSync(playerUid) {
        const ws = this.clients.get(playerUid);
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({
                type: 'ai_sync_request'
            }));
            return true;
        }
        return false;
    }
    
    getStatus() {
        return {
            port: this.port,
            clientCount: this.clients.size,
            clients: Array.from(this.clients.keys())
        };
    }
    
    stop() {
        if (this.heartbeatInterval) {
            clearInterval(this.heartbeatInterval);
            this.heartbeatInterval = null;
        }
        if (this.wss) {
            this.wss.close();
            this.wss = null;
        }
        console.log('[Bridge] 服务已停止');
    }

    // A* 寻路
    onBridgeGetPath(ws, msg) {
        const { mapId, startX, startY, goalX, goalY } = msg;
        const info = mapId && this.mapInfo.has(mapId) ? this.mapInfo.get(mapId) : this.currentMapInfo;
        if (!info) {
            ws.send(JSON.stringify({ type: 'bridge_path', path: [], error: 'no_map_info' }));
            return;
        }
        const { gridInfo, mapWidth, mapHeight } = info;
        if (!gridInfo || !gridInfo[0]) {
            ws.send(JSON.stringify({ type: 'bridge_path', path: [], error: 'no_grid' }));
            return;
        }

        console.log(`[Bridge] 路径查询: map=${mapId}, size=${mapWidth}x${mapHeight}`);
        console.log(`[Bridge] gridInfo结构: [${typeof gridInfo}] len=${gridInfo.length}, gridInfo[247]=${typeof gridInfo[247]} len=${gridInfo[247]?.length}`);
        console.log(`[Bridge] gridInfo[247][221]=${gridInfo[247]?.[221]}, gridInfo[247][219]=${gridInfo[247]?.[219]}, gridInfo[247][220]=${gridInfo[247]?.[220]}`);

        const sx = Math.floor(startX), sy = Math.floor(startY);
        const gx = Math.floor(goalX), gy = Math.floor(goalY);

        // 校验起点终点
        if (!this.isWalkable(gridInfo, sx, sy, mapWidth, mapHeight) ||
            !this.isWalkable(gridInfo, gx, gy, mapWidth, mapHeight)) {
            ws.send(JSON.stringify({ type: 'bridge_path', path: [], error: 'invalid_pos' }));
            return;
        }

        const path = this.aStarFindPath(sx, sy, gx, gy, gridInfo, mapWidth, mapHeight);
        ws.send(JSON.stringify({ type: 'bridge_path', path }));
    }

    isWalkable(gridInfo, x, y, w, h) {
        if (x < 0 || x >= w || y < 0 || y >= h) return false;
        return gridInfo[x] && gridInfo[x][y] === true;
    }

    aStarFindPath(sx, sy, gx, gy, gridInfo, w, h) {
        const idx = (x, y) => y * w + x;
        const hDist = (ax, ay, bx, by) => Math.abs(ax - bx) + Math.abs(ay - by);
        const open = [];
        const closed = new Set();
        const gScore = {};
        const parent = {};
        const startKey = idx(sx, sy);
        gScore[startKey] = 0;
        open.push({ key: startKey, f: hDist(sx, sy, gx, gy), x: sx, y: sy });

        const dirs = [{x:1,y:0},{x:-1,y:0},{x:0,y:1},{x:0,y:-1}];

        while (open.length > 0) {
            open.sort((a, b) => a.f - b.f);
            const cur = open.shift();
            const ck = cur.key;
            if (cur.x === gx && cur.y === gy) {
                // 重建路径
                const result = [];
                let k = ck;
                while (k !== undefined) {
                    const px = k % w, py = Math.floor(k / w);
                    result.unshift({ x: px, y: py });
                    k = parent[k];
                }
                return result;
            }
            if (closed.has(ck)) continue;
            closed.add(ck);

            for (const d of dirs) {
                const nx = cur.x + d.x, ny = cur.y + d.y;
                if (!this.isWalkable(gridInfo, nx, ny, w, h)) continue;
                const nk = idx(nx, ny);
                if (closed.has(nk)) continue;
                const g = (gScore[ck] || 0) + 1;
                if (g < (gScore[nk] !== undefined ? gScore[nk] : Infinity)) {
                    parent[nk] = ck;
                    gScore[nk] = g;
                    open.push({ key: nk, f: g + hDist(nx, ny, gx, gy), x: nx, y: ny });
                }
            }
        }
        return []; // 不可达
    }

    // ============================================================
    // HTTP API 服务器 (端口 18766)
    // ============================================================

    startHttpServer() {
        this.httpServer = http.createServer((req, res) => {
            // CORS 预检
            if (req.method === 'OPTIONS') {
                res.writeHead(204, {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                });
                res.end();
                return;
            }

            // 强制 JSON 输出
            res.setHeader('Content-Type', 'application/json; charset=utf-8');
            res.setHeader('Access-Control-Allow-Origin', '*');

            const url = req.url.split('?')[0];
            const self = this;

            try {
                if (req.method === 'GET' && url === '/health') {
                    this.httpHealth(res);
                } else if (req.method === 'GET' && url === '/clients') {
                    this.httpListClients(res);
                } else if (req.method === 'GET' && url.startsWith('/clients/')) {
                    const parts = url.split('/');
                    if (parts[3] === 'perception') {
                        this.httpGetPerception(parts[2], res);
                    } else if (parts[3] === 'mapInfo') {
                        this.httpGetMapInfo(parts[2], res);
                    } else {
                        this.httpNotFound(res, url);
                    }
                } else if (req.method === 'GET' && url.startsWith('/mapId/')) {
                    const mapId = parseInt(url.split('/')[2]);
                    if (!isNaN(mapId)) {
                        this.httpGetTransportPoints(mapId, res);
                    } else {
                        this.httpError(res, 400, 'Invalid mapId');
                    }
                } else if (req.method === 'POST' && url === '/command') {
                    let body = '';
                    req.on('data', chunk => { body += chunk; });
                    req.on('end', () => {
                        try {
                            const data = JSON.parse(body);
                            self.httpSendCommand(data.playerUid, data.command, res);
                        } catch (e) {
                            self.httpError(res, 400, 'Invalid JSON: ' + e.message);
                        }
                    });
                } else if (req.method === 'POST' && url === '/perception/request') {
                    let body = '';
                    req.on('data', chunk => { body += chunk; });
                    req.on('end', () => {
                        try {
                            const data = JSON.parse(body);
                            self.httpRequestPerception(data.playerUid, data.category, res);
                        } catch (e) {
                            self.httpError(res, 400, 'Invalid JSON: ' + e.message);
                        }
                    });
                } else {
                    this.httpNotFound(res, url);
                }
            } catch (e) {
                this.httpError(res, 500, 'Internal error: ' + e.message);
            }
        });

        this.httpServer.listen(this.httpPort, '127.0.0.1', () => {
            console.log(`[Bridge] HTTP API 已启动: http://localhost:${this.httpPort}`);
        });

        this.httpServer.on('error', (err) => {
            console.error('[Bridge] HTTP 服务器错误:', err.message);
        });
    }

    // GET /health
    httpHealth(res) {
        const gameClients = Array.from(this.clients.keys()).filter(k => !k.startsWith('OPENCLAW'));
        res.end(JSON.stringify({
            status: 'ok',
            uptime: Date.now() - (this.startTime || Date.now()),
            clients: gameClients.length,
            playerUids: gameClients,
            wsPort: this.port,
            httpPort: this.httpPort
        }));
    }

    // GET /clients
    httpListClients(res) {
        const gameClients = Array.from(this.clients.entries())
            .filter(([k]) => !k.startsWith('OPENCLAW'))
            .map(([playerUid, ws]) => ({
                playerUid,
                connected: ws.readyState === WebSocket.OPEN
            }));
        res.end(JSON.stringify({ clients: gameClients }));
    }

    // GET /clients/:playerUid/perception
    httpGetPerception(playerUid, res) {
        if (!playerUid) {
            // 找第一个游戏客户端
            playerUid = Array.from(this.clients.keys()).find(k => !k.startsWith('OPENCLAW'));
        }
        if (!playerUid) {
            res.end(JSON.stringify({ error: '没有已注册的游戏客户端' }));
            return;
        }
        const cache = this.perceptionCache ? this.perceptionCache.get(playerUid) : null;
        if (!cache) {
            res.end(JSON.stringify({ playerUid, error: '暂无感知缓存，请先等待客户端发送感知数据' }));
            return;
        }
        res.end(JSON.stringify({
            playerUid,
            perception: {
                self: cache.self,
                mapId: cache.mapId,
                position: cache.position,
                robots: Array.from(cache.robots.values()),
                players: Array.from(cache.players.values()),
                monsters: Array.from(cache.monsters.values()),
                npcs: Array.from(cache.npcs.values()),
                mapInfor: cache.mapInfor,
                transNodes: cache.transNodes
            },
            timestamp: Date.now()
        }));
    }

    // GET /clients/:playerUid/mapInfo
    httpGetMapInfo(playerUid, res) {
        if (!playerUid) {
            playerUid = Array.from(this.clients.keys()).find(k => !k.startsWith('OPENCLAW'));
        }
        if (!playerUid) {
            res.end(JSON.stringify({ error: '没有已注册的游戏客户端' }));
            return;
        }
        const cache = this.perceptionCache ? this.perceptionCache.get(playerUid) : null;
        if (!cache || !cache.mapInfor) {
            // 尝试从 mapInfo 缓存获取
            const mapId = this.currentMapId;
            const info = mapId && this.mapInfo.has(mapId) ? this.mapInfo.get(mapId) : null;
            res.end(JSON.stringify({ playerUid, mapInfor: info || null }));
            return;
        }
        res.end(JSON.stringify({ playerUid, mapInfor: cache.mapInfor }));
    }

    // GET /mapId/:mapId/transportPoints
    httpGetTransportPoints(mapId, res) {
        const points = this.transportPoints.get(mapId);
        if (!points) {
            res.end(JSON.stringify({ mapId, transportPoints: [], error: '暂无传送门缓存' }));
            return;
        }
        res.end(JSON.stringify({ mapId, transportPoints: points.transportPoints || [] }));
    }

    // POST /command  { playerUid, command }
    httpSendCommand(playerUid, command, res) {
        if (!playerUid || !command) {
            this.httpError(res, 400, '缺少 playerUid 或 command 参数');
            return;
        }
        const targetWs = this.clients.get(playerUid);
        if (!targetWs || targetWs.readyState !== WebSocket.OPEN) {
            this.httpError(res, 404, `玩家不在线: ${playerUid}`);
            return;
        }
        targetWs.send(JSON.stringify({
            type: 'ai_control',
            playerUid: playerUid,
            command: command
        }));
        console.log(`[Bridge] [HTTP] 发送指令到 ${playerUid}:`, JSON.stringify(command));
        res.end(JSON.stringify({ ok: true, playerUid, command }));
    }

    // POST /perception/request { playerUid, category }
    httpRequestPerception(playerUid, category, res) {
        if (!playerUid) {
            playerUid = Array.from(this.clients.keys()).find(k => !k.startsWith('OPENCLAW'));
        }
        if (!playerUid) {
            this.httpError(res, 404, '没有已注册的游戏客户端');
            return;
        }
        const targetWs = this.clients.get(playerUid);
        if (!targetWs || targetWs.readyState !== WebSocket.OPEN) {
            this.httpError(res, 404, `玩家不在线: ${playerUid}`);
            return;
        }
        // 构造感知请求命令
        const catMap = {
            robots: 'getPerception_robots_toBridge',
            npcs: 'getPerception_npcs_toBridge',
            monsters: 'getPerception_monsters_toBridge',
            players: 'getPerception_players_toBridge',
            mapInfor: 'getPerception_mapInfor_toBridge',
            transNodes: 'getPerception_transNodes_toBridge',
            self: 'getPerception_self_toBridge'
        };
        const cmdType = category && catMap[category] ? catMap[category] : 'get_perception';
        targetWs.send(JSON.stringify({
            type: 'ai_control',
            playerUid: playerUid,
            command: { type: cmdType }
        }));
        console.log(`[Bridge] [HTTP] 请求感知: ${playerUid} category=${category || 'all'}`);
        res.end(JSON.stringify({ ok: true, playerUid, category: category || 'all', cmdType }));
    }

    httpNotFound(res, path) {
        res.writeHead(404, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Not Found', path: path || '/' }));
    }

    httpError(res, code, message) {
        res.writeHead(code, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: message }));
    }
}

module.exports = OpenClawGameBridge;
