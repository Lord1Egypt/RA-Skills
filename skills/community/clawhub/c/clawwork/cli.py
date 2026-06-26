#!/usr/bin/env python3
"""
ClawWork Skill - CLI para execução de tarefas profissionais
"""

import os
import sys
import json
import asyncio
import argparse
from pathlib import Path
from datetime import datetime

# Adiciona o ClawWork ao path
CLAWWORK_PATH = Path("/home/freedom/.openclaw/workspace/ClawWork")
sys.path.insert(0, str(CLAWWORK_PATH))
sys.path.insert(0, str(CLAWWORK_PATH / "livebench"))

# Carrega variáveis de ambiente
from dotenv import load_dotenv
load_dotenv(CLAWWORK_PATH / ".env")

def check_setup():
    """Verifica se o setup está completo"""
    required = ["OPENAI_API_KEY", "OPENAI_API_BASE"]
    missing = [var for var in required if not os.getenv(var)]
    if missing:
        print(f"❌ Variáveis faltando: {', '.join(missing)}")
        print(f"   Configure em: {CLAWWORK_PATH}/.env")
        return False
    return True

def create_inline_config(task_description: str, model: str = "zai/glm-4.7") -> dict:
    """Cria configuração inline para uma tarefa específica"""
    
    # Mapeamento simples de tarefa para setor/ocupação
    task_lower = task_description.lower()
    if any(word in task_lower for word in ["código", "software", "api", "sistema", "programa"]):
        sector = "Technology"
        occupation = "Software Engineer"
    elif any(word in task_lower for word in ["marketing", "campanha", "anúncio", "mídia"]):
        sector = "Marketing"
        occupation = "Marketing Manager"
    elif any(word in task_lower for word in ["finanças", "análise", "investimento", "budget"]):
        sector = "Finance"
        occupation = "Financial Analyst"
    elif any(word in task_lower for word in ["dados", "dataset", "modelo", "previsão", "ml"]):
        sector = "Technology"
        occupation = "Data Scientist"
    elif any(word in task_lower for word in ["saúde", "hospital", "paciente", "clínica"]):
        sector = "Healthcare"
        occupation = "Healthcare Administrator"
    else:
        sector = "Professional Services"
        occupation = "Business Analyst"
    
    return {
        "livebench": {
            "date_range": {
                "init_date": datetime.now().strftime("%Y-%m-%d"),
                "end_date": datetime.now().strftime("%Y-%m-%d")
            },
            "economic": {
                "initial_balance": 100.0,
                "task_values_path": None,
                "token_pricing": {
                    "input_per_1m": 0.4,
                    "output_per_1m": 1.5
                },
                "max_work_payment": 50.0
            },
            "agents": [{
                "signature": f"clawwork-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                "basemodel": model,
                "enabled": True,
                "tasks_per_day": 1,
                "supports_multimodal": False
            }],
            "agent_params": {
                "max_steps": 15,
                "max_retries": 3,
                "base_delay": 0.5,
                "tasks_per_day": 1
            },
            "evaluation": {
                "use_llm_evaluation": True,
                "meta_prompts_dir": "./eval/meta_prompts"
            },
            "data_path": "./livebench/data/agent_data",
            "task_source": {
                "type": "inline",
                "tasks": [{
                    "task_id": f"clawwork-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "sector": sector,
                    "occupation": occupation,
                    "prompt": task_description,
                    "reference_files": []
                }]
            }
        }
    }

async def run_task(task_description: str, model: str = "zai/glm-4.7"):
    """Executa uma tarefa do ClawWork"""
    
    if not check_setup():
        return None
    
    # Cria configuração temporária
    config = create_inline_config(task_description, model)
    
    # Salva configuração temporária
    config_path = CLAWWORK_PATH / "livebench" / "configs" / "_temp_clawwork.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"🎯 ClawWork Task Execution")
    print(f"=" * 60)
    print(f"📋 Tarefa: {task_description[:60]}...")
    print(f"🤖 Modelo: {model}")
    print(f"💰 Balance inicial: $100.00")
    print(f"💸 Token pricing: $0.40/1M input, $1.50/1M output")
    print("")
    
    try:
        # Importa e executa o agente
        from agent.live_agent import LiveAgent
        
        lb_config = config["livebench"]
        agent_config = lb_config["agents"][0]
        
        agent = LiveAgent(
            signature=agent_config["signature"],
            basemodel=agent_config["basemodel"],
            init_balance=lb_config["economic"]["initial_balance"],
            config=config
        )
        
        await agent.initialize()
        
        init_date = lb_config["date_range"]["init_date"]
        end_date = lb_config["date_range"]["end_date"]
        
        await agent.run_date_range(init_date, end_date)
        
        # Coleta resultados
        final_balance = agent.economic_tracker.current_balance
        total_cost = agent.economic_tracker.total_cost
        total_earned = agent.economic_tracker.total_earned
        
        print(f"")
        print(f"=" * 60)
        print(f"✅ Tarefa completada!")
        print(f"=" * 60)
        print(f"💰 Balance final: ${final_balance:.2f}")
        print(f"💸 Custo total: ${total_cost:.2f}")
        print(f"💵 Ganhos: ${total_earned:.2f}")
        print(f"📊 Lucro: ${final_balance - lb_config['economic']['initial_balance']:.2f}")
        
        if agent.completed_tasks:
            print(f"")
            print(f"📄 Resultados:")
            for task in agent.completed_tasks:
                print(f"   - {task.get('task_id', 'unknown')}: {task.get('status', 'unknown')}")
        
        return {
            "success": True,
            "balance": final_balance,
            "cost": total_cost,
            "earned": total_earned,
            "tasks": agent.completed_tasks
        }
        
    except Exception as e:
        print(f"")
        print(f"❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}
    
    finally:
        # Limpa configuração temporária
        if config_path.exists():
            config_path.unlink()

def show_status():
    """Mostra status dos agentes ClawWork"""
    data_path = CLAWWORK_PATH / "livebench" / "data" / "agent_data"
    
    if not data_path.exists():
        print("📊 Nenhum dado de agente encontrado")
        return
    
    print("📊 ClawWork Agent Status")
    print("=" * 60)
    
    for agent_dir in data_path.iterdir():
        if agent_dir.is_dir():
            print(f"")
            print(f"🤖 Agente: {agent_dir.name}")
            
            # Procura por arquivos de log
            logs_dir = agent_dir / "activity_logs"
            if logs_dir.exists():
                dates = sorted([d.name for d in logs_dir.iterdir() if d.is_dir()])
                if dates:
                    print(f"   📅 Período: {dates[0]} a {dates[-1]}")
                    print(f"   📁 Logs: {len(dates)} dias")

def compare_models():
    """Compara performance de modelos"""
    print("🏆 ClawWork Model Comparison")
    print("=" * 60)
    print("")
    print("Modelos disponíveis para teste:")
    print("  - zai/glm-4.7 (nosso default)")
    print("  - kimi-coding/k2p5 (o que uso agora)")
    print("  - qwen-portal/coder-model")
    print("  - openai/gpt-4o")
    print("")
    print("Para comparar, execute:")
    print("  python -m clawwork.cli run 'tarefa' --model zai/glm-4.7")
    print("  python -m clawwork.cli run 'tarefa' --model kimi-coding/k2p5")

def main():
    parser = argparse.ArgumentParser(description="ClawWork Skill CLI")
    parser.add_argument("command", choices=["run", "status", "compare"], help="Comando a executar")
    parser.add_argument("--task", "-t", help="Descrição da tarefa")
    parser.add_argument("--model", "-m", default="zai/glm-4.7", help="Modelo a usar")
    
    args = parser.parse_args()
    
    if args.command == "run":
        if not args.task:
            print("❌ Especifique a tarefa com --task ou -t")
            print("Exemplo: python -m clawwork.cli run -t 'Criar análise de mercado'")
            sys.exit(1)
        
        result = asyncio.run(run_task(args.task, args.model))
        sys.exit(0 if result and result.get("success") else 1)
    
    elif args.command == "status":
        show_status()
    
    elif args.command == "compare":
        compare_models()

if __name__ == "__main__":
    main()
