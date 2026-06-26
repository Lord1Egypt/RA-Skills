#!/usr/bin/env python3
"""
AHC-Automator Utilities
Classes e funções auxiliares para automação AHC
"""

import os
import json
import logging
import subprocess
import re
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path

class AHCConfig:
    """Gerenciador de configuração para AHC-Automator"""
    
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = Path(__file__).parent.parent / 'configs' / 'ahc_config.json'
        
        self.config_path = Path(config_path)
        self.config = self.load_config()
        
    def load_config(self):
        """Carregar configuração do arquivo JSON"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Erro ao carregar configuração: {e}")
            
    def get(self, *keys, default=None):
        """Obter valor de configuração aninhada"""
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value
        
    def get_env_or_config(self, env_key, *config_keys, default=None):
        """Obter valor do ambiente ou configuração"""
        env_value = os.environ.get(env_key)
        if env_value:
            return env_value
        return self.get(*config_keys, default=default)

class ClickUpClient:
    """Cliente ClickUp para operações de API"""
    
    def __init__(self, config):
        self.config = config
        self.api_token = self.config.get_env_or_config('CLICKUP_API_TOKEN', 'clickup', 'api_token')
        self.team_id = self.config.get('clickup', 'team_id')
        self.base_url = self.config.get('clickup', 'api_url', default='https://api.clickup.com/api/v2')
        
        if not self.api_token:
            raise Exception("ClickUp API token não encontrado")
            
    def _request(self, method, endpoint, data=None):
        """Fazer requisição para API ClickUp"""
        url = f"{self.base_url}/{endpoint}"
        
        headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
        
        if data and method in ['POST', 'PUT']:
            data = json.dumps(data).encode('utf-8')
            
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        
        try:
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            return {"success": True, "data": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
            
    def create_task(self, list_id, name, description=None, assignees=None, priority=None, due_date=None):
        """Criar nova task no ClickUp"""
        data = {
            "name": name,
            "description": description or "",
            "priority": priority or 3
        }
        
        if assignees:
            data["assignees"] = assignees
            
        if due_date:
            # Converter due_date para timestamp se necessário
            if isinstance(due_date, str):
                try:
                    due_date = datetime.fromisoformat(due_date).timestamp() * 1000
                except:
                    due_date = None
            data["due_date"] = int(due_date) if due_date else None
            
        return self._request('POST', f'list/{list_id}/task', data)
        
    def get_tasks(self, list_id, limit=10):
        """Obter tasks de uma lista"""
        return self._request('GET', f'list/{list_id}/task?limit={limit}')
        
    def update_task(self, task_id, **kwargs):
        """Atualizar task existente"""
        return self._request('PUT', f'task/{task_id}', kwargs)
        
    def create_list(self, folder_id, name):
        """Criar nova lista no ClickUp"""
        data = {"name": name}
        return self._request('POST', f'folder/{folder_id}/list', data)

class PipedriveClient:
    """Cliente Pipedrive para operações de CRM"""
    
    def __init__(self, config):
        self.config = config
        self.api_token = self.config.get_env_or_config('PIPEDRIVE_API_TOKEN', 'pipedrive', 'api_token')
        self.base_url = self.config.get('pipedrive', 'api_url', default='https://api.pipedrive.com/v1')
        
        if not self.api_token:
            raise Exception("Pipedrive API token não encontrado")
            
        # Remove 'env:' prefix se existir
        if self.api_token.startswith('env:'):
            env_key = self.api_token[4:]
            self.api_token = os.environ.get(env_key)
            
        if not self.api_token:
            raise Exception("Pipedrive API token não configurado corretamente")
            
    def _request(self, method, endpoint, data=None):
        """Fazer requisição para API Pipedrive"""
        url = f"{self.base_url}/{endpoint}"
        
        # Adicionar API token
        separator = '&' if '?' in url else '?'
        url = f"{url}{separator}api_token={self.api_token}"
        
        if data and method in ['POST', 'PUT']:
            data = json.dumps(data).encode('utf-8')
            req = urllib.request.Request(url, data=data, method=method)
            req.add_header('Content-Type', 'application/json')
        else:
            req = urllib.request.Request(url, method=method)
        
        try:
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            return {"success": result.get('success', True), "data": result.get('data')}
        except Exception as e:
            return {"success": False, "error": str(e)}
            
    def create_deal(self, title, value=None, currency='EUR', person_id=None, org_id=None):
        """Criar novo deal"""
        data = {'title': title}
        if value:
            data['value'] = value
        if currency:
            data['currency'] = currency
        if person_id:
            data['person_id'] = person_id
        if org_id:
            data['org_id'] = org_id
            
        return self._request('POST', 'deals', data)
        
    def create_person(self, name, email=None, phone=None, org_id=None):
        """Criar nova pessoa"""
        data = {'name': name}
        if email:
            data['email'] = [email] if isinstance(email, str) else email
        if phone:
            data['phone'] = [phone] if isinstance(phone, str) else phone
        if org_id:
            data['org_id'] = org_id
            
        return self._request('POST', 'persons', data)
        
    def search_persons(self, term):
        """Buscar pessoas"""
        return self._request('GET', f'persons/search?term={urllib.parse.quote(term)}')
        
    def create_or_find_person(self, name, email=None, phone=None):
        """Criar ou encontrar pessoa existente"""
        # Primeiro tentar buscar por nome
        search_result = self.search_persons(name)
        
        if search_result.get('success') and search_result.get('data'):
            # Se encontrou, retornar a primeira pessoa
            return {"success": True, "data": search_result['data'][0]}
            
        # Se não encontrou, criar nova pessoa
        return self.create_person(name, email, phone)

class WhatsAppNotifier:
    """Notificador WhatsApp para AHC workflows"""
    
    def __init__(self, config):
        self.config = config
        self.enabled = True  # Pode ser configurado para desabilitar notificações
        
    def send_notification(self, message, link=None):
        """Enviar notificação WhatsApp"""
        if not self.enabled:
            return
            
        try:
            # Por enquanto, apenas log da notificação
            # Implementação real depende do sistema WhatsApp disponível
            full_message = message
            if link:
                full_message += f"\n🔗 {link}"
                
            logging.info(f"WhatsApp Notification: {full_message}")
            
            # TODO: Implementar envio real via WhatsApp API ou OpenClaw message tool
            
        except Exception as e:
            logging.error(f"Erro ao enviar notificação WhatsApp: {e}")

class EmailParser:
    """Parser de emails para extrair dados estruturados"""
    
    def __init__(self, config):
        self.config = config
        self.clickup_keywords = self.config.get('email', 'keywords', 'clickup', default=[])
        self.pipedrive_keywords = self.config.get('email', 'keywords', 'pipedrive', default=[])
        
    def get_recent_emails(self, accounts, since_time):
        """Obter emails recentes das contas monitoradas"""
        emails = []
        
        try:
            # Usar AppleScript para acessar Apple Mail
            for account in accounts:
                script = f'''
                tell application "Mail"
                    set recentEmails to {{}}
                    repeat with theAccount in accounts
                        if (name of theAccount) contains "{account}" then
                            repeat with theMailbox in mailboxes of theAccount
                                repeat with theMessage in messages of theMailbox
                                    set messageDate to date received of theMessage
                                    if messageDate > (current date) - (5 * minutes) then
                                        set end of recentEmails to {{subject:(subject of theMessage), sender:(sender of theMessage as string), content:(content of theMessage), date_received:messageDate}}
                                    end if
                                end repeat
                            end repeat
                        end if
                    end repeat
                    return recentEmails
                end tell
                '''
                
                result = subprocess.run(['osascript', '-e', script], 
                                      capture_output=True, text=True)
                
                if result.returncode == 0:
                    # Parsear resultado do AppleScript
                    # Isso é uma simplificação - implementação real seria mais robusta
                    pass
                    
        except Exception as e:
            logging.error(f"Erro ao obter emails: {e}")
            
        # Retornar dados de exemplo para teste
        return [
            {
                'sender': 'ian@alanharpercomposites.com.br',
                'subject': 'Nova tarefa ClickUp',
                'body': 'Preciso adicionar tarefa para revisar lista de convidados',
                'date_received': datetime.now()
            }
        ]
        
    def contains_keywords(self, email, keyword_type):
        """Verificar se email contém keywords específicas"""
        keywords = self.clickup_keywords if keyword_type == 'clickup' else self.pipedrive_keywords
        
        text_to_check = f"{email.get('subject', '')} {email.get('body', '')}".lower()
        
        return any(keyword.lower() in text_to_check for keyword in keywords)
        
    def extract_clickup_data(self, email):
        """Extrair dados estruturados para ClickUp"""
        subject = email.get('subject', '')
        body = email.get('body', '')
        
        # Lógica de extração baseada em padrões
        data = {
            'name': subject if subject else 'Nova tarefa por email',
            'description': body,
            'assignees': [],
            'priority': 3
        }
        
        # Detectar lista específica baseada no conteúdo
        if 'lista de convidados' in body.lower():
            data['list_id'] = self.config.get('clickup', 'templates', 'birthday_list')
        else:
            data['list_id'] = self.config.get('clickup', 'templates', 'standard')
            
        return data
        
    def extract_pipedrive_data(self, email):
        """Extrair dados estruturados para Pipedrive"""
        subject = email.get('subject', '')
        body = email.get('body', '')
        
        # Padrões regex para extrair informações
        name_pattern = r'cliente:?\s*([A-Za-zÀ-ÿ\s]+)'
        email_pattern = r'email:?\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
        value_pattern = r'valor:?\s*€?([0-9.,]+)'
        
        data = {
            'deal_title': subject if 'deal' in subject.lower() else f'Oportunidade de {email.get("sender", "")}',
            'person_name': None,
            'person_email': None,
            'value': None,
            'currency': 'EUR'
        }
        
        # Extrair nome
        name_match = re.search(name_pattern, body, re.IGNORECASE)
        if name_match:
            data['person_name'] = name_match.group(1).strip()
            
        # Extrair email
        email_match = re.search(email_pattern, body)
        if email_match:
            data['person_email'] = email_match.group(1)
            
        # Extrair valor
        value_match = re.search(value_pattern, body, re.IGNORECASE)
        if value_match:
            value_str = value_match.group(1).replace(',', '.')
            try:
                data['value'] = float(value_str)
            except:
                data['value'] = None
                
        return data