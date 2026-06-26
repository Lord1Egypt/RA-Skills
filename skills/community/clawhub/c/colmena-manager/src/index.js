#!/usr/bin/env node

import { exec, process, agents_list, sessions_list, sessions_send, message } from 'openclaw';

interface Agent {
  id: string;
  name: string;
  status: string;
  workspace: string;
}

interface Session {
  id: string;
  agentId: string;
  status: string;
  startedAt: string;
}

class ColmenaManager {
  async status(agentId?: string): Promise<void> {
    const agents = await agents_list();
    
    if (agentId) {
      const agent = agents.find(a => a.id === agentId);
      if (!agent) {
        console.log(`Agente ${agentId} no encontrado`);
        return;
      }
      
      const sessions = await sessions_list({ agentId });
      console.log(`Agente: ${agent.name} (${agent.id})`);
      console.log(`Estado: ${agent.status}`);
      console.log(`Workspace: ${agent.workspace}`);
      console.log(`Sesiones activas: ${sessions.length}`);
      
      if (sessions.length > 0) {
        console.log("\nSesiones:");
        sessions.forEach(s => {
          console.log(`  - ${s.id}: ${s.status} desde ${s.startedAt}`);
        });
      }
    } else {
      console.log("Colmena - Estado de todos los agentes:");
      agents.forEach(agent => {
        console.log(`${agent.id}: ${agent.name} - ${agent.status}`);
      });
    }
  }

  async broadcast(message: string): Promise<void> {
    const agents = await agents_list();
    console.log(`Enviando broadcast a ${agents.length} agentes...`);
    
    for (const agent of agents) {
      try {
        await sessions_send({ 
          agentId: agent.id, 
          message: `BROADCAST: ${message}` 
        });
        console.log(`  - ${agent.name}: OK`);
      } catch (error) {
        console.log(`  - ${agent.name}: ERROR (${error})`);
      }
    }
  }

  async logs(agentId: string, lines: number = 50): Promise<void> {
    try {
      const result = await exec({
        command: `tail -n ${lines} /home/nvi/.openclaw/sessions/${agentId}/logs.txt`,
        timeout: 5
      });
      console.log(`Logs de ${agentId} (últimas ${lines} líneas):`);
      console.log(result.stdout);
    } catch (error) {
      console.log(`Error al obtener logs: ${error}`);
    }
  }

  async pause(agentId: string): Promise<void> {
    try {
      await sessions_send({
        agentId,
        message: "PAUSAR"
      });
      console.log(`Agente ${agentId} pausado`);
    } catch (error) {
      console.log(`Error al pausar: ${error}`);
    }
  }

  async resume(agentId: string): Promise<void> {
    try {
      await sessions_send({
        agentId,
        message: "REANUDAR"
      });
      console.log(`Agente ${agentId} reanudado`);
    } catch (error) {
      console.log(`Error al reanudar: ${error}`);
    }
  }

  async healthCheck(): Promise<void> {
    const agents = await agents_list();
    console.log("HealthCheck - Estado de la Colmena:");
    console.log("="".repeat(30));
    
    let allHealthy = true;
    
    for (const agent of agents) {
      console.log(`\n${agent.name} (${agent.id}):`);
      
      // Check sesiones
      try {
        const sessions = await sessions_list({ agentId: agent.id });
        console.log(`  Sesiones: ${sessions.length} activas`);
      } catch (error) {
        console.log(`  ERROR sesiones: ${error}`);
        allHealthy = false;
      }
      
      // Check proceso
      try {
        const result = await exec({
          command: `ps aux | grep ${agent.id} | grep -v grep | wc -l`,
          timeout: 3
        });
        const count = parseInt(result.stdout.trim());
        console.log(`  Proceso: ${count > 0 ? "ACTIVO" : "INACTIVO"}`);
        if (count === 0) allHealthy = false;
      } catch (error) {
        console.log(`  ERROR proceso: ${error}`);
        allHealthy = false;
      }
      
      // Check memoria
      try {
        const memory = await this.checkMemory(agent.id);
        console.log(`  Memoria: ${memory.used}/${memory.total} MB`);
      } catch (error) {
        console.log(`  ERROR memoria: ${error}`);
        allHealthy = false;
      }
    }
    
    console.log("\nResumen:");
    console.log(`Estado: ${allHealthy ? "✅ SALUDABLE" : "⚠️  ADVERTENCIA"}`);
    console.log(`Agentes: ${agents.length}`);
  }

  async checkMemory(agentId: string): Promise<{used: number; total: number}> {
    const result = await exec({
      command: `ps aux | grep ${agentId} | grep -v grep | awk '{sum+=$6} END {print sum}'`,
      timeout: 3
    });
    const usedMB = parseInt(result.stdout.trim()) / 1024;
    
    return {
      used: Math.round(usedMB),
      total: 2048 // Asumir 2GB por defecto
    };
  }

  async workspaceList(): Promise<void> {
    try {
      const result = await exec({
        command: `ls -la /home/nvi/.openclaw/workspace-*`,
        timeout: 5
      });
      console.log("Workspaces disponibles:");
      console.log(result.stdout);
    } catch (error) {
      console.log(`Error: ${error}`);
    }
  }

  async workspaceCreate(name: string): Promise<void> {
    try {
      await exec({
        command: `mkdir -p /home/nvi/.openclaw/workspace-${name}`,
        timeout: 5
      });
      console.log(`Workspace ${name} creado`);
    } catch (error) {
      console.log(`Error: ${error}`);
    }
  }

  async workspaceRemove(name: string): Promise<void> {
    try {
      await exec({
        command: `rm -rf /home/nvi/.openclaw/workspace-${name}`,
        timeout: 10
      });
      console.log(`Workspace ${name} eliminado`);
    } catch (error) {
      console.log(`Error: ${error}`);
    }
  }
}

// CLI Handler
const manager = new ColmenaManager();

const args = process.argv.slice(2);

if (args.length === 0) {
  console.log("Colmena Manager - Gestiona tu colmena de agentes");
  console.log("Uso: colmena-manager <comando> [opciones]");
  console.log("\nComandos:");
  console.log("  status [agent]     - Ver estado de agentes");
  console.log("  broadcast <msg>    - Enviar mensaje a todos");
  console.log("  logs <agent> [n]   - Ver logs (50 por defecto)");
  console.log("  pause <agent>      - Pausar agente");
  console.log("  resume <agent>     - Reanudar agente");
  console.log("  health-check       - Verificar salud de la colmena");
  console.log("  workspace list     - Listar workspaces");
  console.log("  workspace create <name>");
  console.log("  workspace remove <name>");
} else {
  const command = args[0];
  
  switch (command) {
    case "status":
      manager.status(args[1]);
      break;
    case "broadcast":
      if (args.length < 2) {
        console.log("Uso: broadcast <mensaje>");
      } else {
        manager.broadcast(args.slice(1).join(" "));
      }
      break;
    case "logs":
      if (args.length < 2) {
        console.log("Uso: logs <agent> [líneas]");
      } else {
        const lines = args.length > 2 ? parseInt(args[2]) : 50;
        manager.logs(args[1], lines);
      }
      break;
    case "pause":
      if (args.length < 2) {
        console.log("Uso: pause <agent>");
      } else {
        manager.pause(args[1]);
      }
      break;
    case "resume":
      if (args.length < 2) {
        console.log("Uso: resume <agent>");
      } else {
        manager.resume(args[1]);
      }
      break;
    case "health-check":
      manager.healthCheck();
      break;
    case "workspace":
      if (args.length < 2) {
        console.log("Uso: workspace <comando> [nombre]");
      } else {
        switch (args[1]) {
          case "list":
            manager.workspaceList();
            break;
          case "create":
            if (args.length < 3) {
              console.log("Uso: workspace create <nombre>");
            } else {
              manager.workspaceCreate(args[2]);
            }
            break;
          case "remove":
            if (args.length < 3) {
              console.log("Uso: workspace remove <nombre>");
            } else {
              manager.workspaceRemove(args[2]);
            }
            break;
          default:
            console.log("Comando workspace no reconocido");
        }
      }
      break;
    default:
      console.log(`Comando desconocido: ${command}`);
  }
}