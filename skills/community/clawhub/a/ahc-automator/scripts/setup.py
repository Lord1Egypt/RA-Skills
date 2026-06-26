#!/usr/bin/env python3
"""
AHC-Automator: Setup e Instalação
Script de configuração inicial para AHC-Automator skill
"""

import os
import sys
import json
import logging
import subprocess
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent

class AHCSetup:
    """Configurador inicial para AHC-Automator"""
    
    def __init__(self):
        self.skill_dir = SKILL_DIR
        self.config_file = self.skill_dir / 'configs' / 'ahc_config.json'
        self.logs_dir = Path.home() / '.openclaw' / 'workspace' / 'logs' / 'ahc-automator'
        
    def run_setup(self, interactive=True):
        """Executar setup completo"""
        print("🔧 AHC-Automator Setup")
        print("=" * 50)
        
        results = []
        
        # 1. Criar diretórios necessários
        print("\n1. Criando diretórios...")
        dir_result = self.create_directories()
        results.append(("Diretórios", dir_result))
        
        # 2. Verificar dependências
        print("\n2. Verificando dependências...")
        deps_result = self.check_dependencies()
        results.append(("Dependências", deps_result))
        
        # 3. Configurar variáveis de ambiente
        if interactive:
            print("\n3. Configurando variáveis de ambiente...")
            env_result = self.setup_environment_interactive()
            results.append(("Variáveis de ambiente", env_result))
        
        # 4. Configurar webhooks/cron jobs se necessário
        print("\n4. Verificando automações existentes...")
        automation_result = self.check_existing_automations()
        results.append(("Automações", automation_result))
        
        # 5. Teste de conectividade
        print("\n5. Testando conectividade...")
        connectivity_result = self.test_connectivity()
        results.append(("Conectividade", connectivity_result))
        
        # 6. Relatório final
        print("\n" + "="*50)
        print("📊 RELATÓRIO DE SETUP")
        print("="*50)
        
        all_success = True
        for check_name, success in results:
            status = "✅ OK" if success else "❌ ERRO"
            print(f"{check_name}: {status}")
            if not success:
                all_success = False
                
        if all_success:
            print("\n🎉 Setup concluído com sucesso!")
            print("\n📚 Próximos passos:")
            print("  1. Execute: python scripts/health_check.py")
            print("  2. Teste: python scripts/email_to_clickup_pipedrive.py --debug")
            print("  3. Leia: docs/README.md")
            return True
        else:
            print("\n⚠️  Setup concluído com algumas pendências.")
            print("   Revise os erros acima antes de usar o sistema.")
            return False
            
    def create_directories(self):
        """Criar diretórios necessários"""
        try:
            directories = [
                self.logs_dir,
                self.skill_dir / 'docs',
                self.skill_dir / 'templates',
                self.skill_dir / 'workflows',
                Path.home() / '.openclaw' / 'workspace' / 'reports'
            ]
            
            for directory in directories:
                directory.mkdir(parents=True, exist_ok=True)
                print(f"  📁 {directory}")
                
            return True
            
        except Exception as e:
            print(f"  ❌ Erro ao criar diretórios: {e}")
            return False
            
    def check_dependencies(self):
        """Verificar dependências do sistema"""
        try:
            # Verificar Python
            python_version = sys.version_info
            if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
                print(f"  ❌ Python 3.8+ necessário (atual: {python_version.major}.{python_version.minor})")
                return False
            else:
                print(f"  ✅ Python {python_version.major}.{python_version.minor}")
                
            # Verificar OpenClaw
            try:
                result = subprocess.run(['openclaw', '--version'], capture_output=True, text=True)
                if result.returncode == 0:
                    print("  ✅ OpenClaw instalado")
                else:
                    print("  ❌ OpenClaw não encontrado")
                    return False
            except FileNotFoundError:
                print("  ❌ OpenClaw não encontrado no PATH")
                return False
                
            # Verificar osascript (para Apple Mail)
            try:
                result = subprocess.run(['osascript', '-e', 'tell application "System Events" to return name'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print("  ✅ AppleScript disponível")
                else:
                    print("  ⚠️  AppleScript com problemas (email automation pode não funcionar)")
            except FileNotFoundError:
                print("  ⚠️  AppleScript não encontrado (email automation não funcionará)")
                
            return True
            
        except Exception as e:
            print(f"  ❌ Erro ao verificar dependências: {e}")
            return False
            
    def setup_environment_interactive(self):
        """Configurar variáveis de ambiente interativamente"""
        try:
            print("  Configure as seguintes variáveis de ambiente:")
            
            env_vars = [
                {
                    'name': 'CLICKUP_API_TOKEN',
                    'description': 'Token da API ClickUp',
                    'required': True,
                    'help': 'Obtenha em: ClickUp → Settings → Apps → API'
                },
                {
                    'name': 'PIPEDRIVE_API_TOKEN', 
                    'description': 'Token da API Pipedrive',
                    'required': True,
                    'help': 'Obtenha em: Pipedrive → Settings → Personal Preferences → API'
                }
            ]
            
            shell_commands = []
            
            for var in env_vars:
                current_value = os.environ.get(var['name'])
                
                if current_value:
                    print(f"  ✅ {var['name']}: já configurado")
                else:
                    print(f"\n  🔑 {var['description']}")
                    print(f"     {var['help']}")
                    
                    value = input(f"     Digite {var['name']}: ").strip()
                    
                    if value:
                        # Adicionar ao shell profile
                        shell_commands.append(f'export {var["name"]}="{value}"')
                        os.environ[var['name']] = value  # Para esta sessão
                        print(f"  ✅ {var['name']} configurado")
                    else:
                        if var['required']:
                            print(f"  ❌ {var['name']} é obrigatório")
                            return False
                        else:
                            print(f"  ⚠️  {var['name']} não configurado")
                            
            # Salvar no shell profile se houver mudanças
            if shell_commands:
                self.save_to_shell_profile(shell_commands)
                
            return True
            
        except Exception as e:
            print(f"  ❌ Erro na configuração de ambiente: {e}")
            return False
            
    def save_to_shell_profile(self, commands):
        """Salvar comandos no profile do shell"""
        try:
            # Detectar shell
            shell = os.environ.get('SHELL', '/bin/bash')
            
            if 'zsh' in shell:
                profile_file = Path.home() / '.zshrc'
            else:
                profile_file = Path.home() / '.bash_profile'
                
            print(f"\n  📝 Adicionando ao {profile_file}")
            
            with open(profile_file, 'a') as f:
                f.write('\n# AHC-Automator Environment Variables\n')
                for cmd in commands:
                    f.write(f'{cmd}\n')
                    
            print(f"  ✅ Variáveis adicionadas ao {profile_file}")
            print(f"  ⚠️  Execute: source {profile_file}")
            
        except Exception as e:
            print(f"  ❌ Erro ao salvar no profile: {e}")
            
    def check_existing_automations(self):
        """Verificar automações existentes"""
        try:
            print("  Verificando cron jobs existentes...")
            
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            
            if result.returncode == 0:
                cron_content = result.stdout
                
                # IDs dos cron jobs do TOOLS.md
                expected_jobs = {
                    'Ian ClickUp': '7c4c353d-55dd-4de9-b315-344f68e147e1',
                    'Ronaldo ClickUp': '26e299db-5273-482e-81a6-278667329669',
                    'Ian Pipedrive': '878b8aa3-4dbc-41d1-8497-0c623e8764c3'
                }
                
                found_jobs = 0
                for job_name, job_id in expected_jobs.items():
                    if job_id in cron_content:
                        print(f"  ✅ {job_name}: encontrado")
                        found_jobs += 1
                    else:
                        print(f"  ❌ {job_name}: não encontrado")
                        
                if found_jobs == len(expected_jobs):
                    print("  ✅ Todos os cron jobs estão configurados")
                    return True
                else:
                    print(f"  ⚠️  {found_jobs}/{len(expected_jobs)} cron jobs encontrados")
                    print("     Configure os cron jobs faltantes conforme TOOLS.md")
                    return True  # Não bloqueante
                    
            else:
                print("  ⚠️  Não foi possível verificar cron jobs")
                return True  # Não bloqueante
                
        except Exception as e:
            print(f"  ❌ Erro ao verificar automações: {e}")
            return False
            
    def test_connectivity(self):
        """Testar conectividade com APIs"""
        try:
            # Importar e testar health check
            sys.path.append(str(self.skill_dir))
            from scripts.health_check import AHCHealthChecker
            
            checker = AHCHealthChecker()
            
            # Teste básico de conectividade
            api_check = checker.check_api_connectivity()
            
            if api_check['status'] == 'ok':
                print("  ✅ Conectividade com APIs: OK")
                return True
            else:
                print("  ❌ Problemas de conectividade:")
                for error in api_check.get('errors', []):
                    print(f"     • {error}")
                return False
                
        except Exception as e:
            print(f"  ❌ Erro no teste de conectividade: {e}")
            return False

def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AHC-Automator Setup')
    parser.add_argument('--non-interactive', action='store_true', help='Executar sem interação')
    parser.add_argument('--check-only', action='store_true', help='Apenas verificar status')
    
    args = parser.parse_args()
    
    try:
        setup = AHCSetup()
        
        if args.check_only:
            # Apenas verificar status atual
            print("🔍 Verificando status atual...")
            sys.path.append(str(SKILL_DIR))
            from scripts.health_check import AHCHealthChecker
            
            checker = AHCHealthChecker()
            results = checker.run_full_health_check()
            
            print(f"\n📊 Status: {results['overall_status'].upper()}")
            if results['overall_status'] != 'ok':
                print("💡 Execute o setup para corrigir problemas:")
                print("   python scripts/setup.py")
        else:
            success = setup.run_setup(interactive=not args.non_interactive)
            
            if success:
                print("\n🚀 AHC-Automator está pronto para uso!")
                sys.exit(0)
            else:
                print("\n❌ Setup incompleto. Corrija os problemas e execute novamente.")
                sys.exit(1)
                
    except KeyboardInterrupt:
        print("\n\n⏹️  Setup cancelado pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()