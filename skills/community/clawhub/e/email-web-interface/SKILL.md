---
name: email-web-interface
description: Web interface for agent email communication (Lourens, Ace, etc.). Provides inbox viewing, draft creation/editing, and sending functionality via Gmail/Gog CLI integration.
---

# Email Web Interface Skill

## Description
Web interface for agent email communication (Lourens, Ace, etc.). Provides inbox viewing, draft creation/editing, and sending functionality via Gmail/Gog CLI integration.

## When to Use
- When user needs to access agent email inboxes
- To compose and send non-bot emails
- To view and manage email drafts
- When existing webmail interfaces are clunky

## Options Considered

### Option A: Existing Webmail Solutions
1. **Roundcube** (Recommended)
   - Pros: Mature, feature-rich, good plugin ecosystem
   - Cons: Can be heavy, PHP-based

2. **RainLoop**
   - Pros: Modern, lightweight, good mobile support
   - Cons: Less mature, fewer features

3. **SnappyMail**
   - Pros: Fast, Gmail-like interface
   - Cons: Newer project, smaller community

### Option B: Custom Interface
Build a custom React/Node.js interface that:
- Uses Gog CLI for Gmail API access
- Provides clean, minimal interface
- Integrates with Mission Control
- Tailored to our specific needs

## Recommended Approach
**Start with Roundcube**, then customize if needed. Roundcube provides:
- Full email functionality out of the box
- IMAP/SMTP support (works with Gmail)
- Plugin system for customization
- Stable and well-documented

## Procedure

### 1. Install Roundcube
```bash
# Install dependencies
apt-get update
apt-get install -y roundcube roundcube-core roundcube-mysql roundcube-plugins

# Or use Docker
docker run -d --name roundcube \
  -p 8081:80 \
  -e ROUNDCUBEMAIL_DEFAULT_HOST=ssl://imap.gmail.com \
  -e ROUNDCUBEMAIL_DEFAULT_PORT=993 \
  -e ROUNDCUBEMAIL_SMTP_SERVER=tls://smtp.gmail.com \
  -e ROUNDCUBEMAIL_SMTP_PORT=587 \
  roundcube/roundcubemail
```

### 2. Configure Gmail Access
Ace's Gmail account needs:
1. **App Password** (if 2FA enabled): Generate in Google Account → Security
2. **IMAP enabled**: Settings → Forwarding and POP/IMAP → Enable IMAP
3. **Less secure apps** (if needed): May require allowing less secure apps

### 3. Roundcube Configuration
```php
// config/config.inc.php
$config['default_host'] = 'ssl://imap.gmail.com';
$config['default_port'] = 993;
$config['smtp_server'] = 'tls://smtp.gmail.com';
$config['smtp_port'] = 587;
$config['smtp_user'] = 'ace.agent.email@gmail.com';
$config['smtp_pass'] = 'APP_PASSWORD_HERE';
$config['imap_conn_options'] = array(
  'ssl' => array(
    'verify_peer' => false,
    'verify_peer_name' => false,
  ),
);
```

### 4. Custom Integration (If Needed)
If Roundcube is clunky, build custom interface:

```python
# Custom email interface using Gog CLI
from flask import Flask, render_template, request, jsonify
import subprocess
import json

app = Flask(__name__)

class EmailInterface:
    def __init__(self):
        self.gog_path = "/usr/local/bin/gog"
    
    def get_inbox(self, limit=50):
        """Get inbox emails via Gog CLI."""
        cmd = [self.gog_path, "gmail", "messages", "list", 
               "--limit", str(limit), "--format", "json"]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                return json.loads(result.stdout)
        except Exception as e:
            print(f"Error getting inbox: {e}")
        
        return []
    
    def get_message(self, message_id):
        """Get specific email message."""
        cmd = [self.gog_path, "gmail", "messages", "get",
               message_id, "--format", "json"]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                return json.loads(result.stdout)
        except Exception as e:
            print(f"Error getting message: {e}")
        
        return None
    
    def send_email(self, to, subject, body):
        """Send email via Gog CLI."""
        cmd = [self.gog_path, "gmail", "messages", "send",
               "--to", to, "--subject", subject, "--body", body]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

@app.route('/')
def inbox():
    """Inbox view."""
    email_iface = EmailInterface()
    messages = email_iface.get_inbox(limit=20)
    return render_template('inbox.html', messages=messages)

@app.route('/message/<message_id>')
def view_message(message_id):
    """View specific message."""
    email_iface = EmailInterface()
    message = email_iface.get_message(message_id)
    return render_template('message.html', message=message)

@app.route('/compose', methods=['GET', 'POST'])
def compose():
    """Compose new email."""
    if request.method == 'POST':
        to = request.form['to']
        subject = request.form['subject']
        body = request.form['body']
        
        email_iface = EmailInterface()
        success = email_iface.send_email(to, subject, body)
        
        return jsonify({'success': success})
    
    return render_template('compose.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=True)
```

### 5. Mission Control Integration
Add email interface to Mission Control sidebar:
```javascript
// mission-control sidebar config
{
  name: "📧 Ace Email",
  path: "/email",
  icon: "email",
  external: true,
  url: "http://localhost:8081"  // Roundcube
  // or: "http://localhost:8082"  // Custom interface
}
```

### 6. Security Considerations
1. **HTTPS**: Use reverse proxy with SSL
2. **Authentication**: Add login to email interface
3. **Rate limiting**: Prevent abuse
4. **Logging**: Monitor email access
5. **Backup**: Regular backup of important emails

## Implementation Steps

### Phase 1: Quick Setup (Today)
1. Install Roundcube via Docker
2. Configure with Ace's Gmail credentials
3. Test basic email functionality
4. Add link to Mission Control

### Phase 2: Customization (This Week)
1. Evaluate Roundcube usability
2. If clunky, start custom interface development
3. Implement essential features:
   - Inbox with threading
   - Compose with rich text
   - Draft saving
   - Search functionality

### Phase 3: Integration (Next Week)
1. Deep integration with Mission Control
2. Notification system for new emails
3. Email templates for common responses
4. Advanced search and filtering

## Testing Checklist
- [ ] Can view inbox
- [ ] Can read emails
- [ ] Can compose new email
- [ ] Can send email
- [ ] Can save drafts
- [ ] Search works
- [ ] Mobile responsive
- [ ] Secure (HTTPS, auth)

## Fallback Plan
If Roundcube doesn't work well:
1. Try RainLoop (lighter alternative)
2. Build minimal custom interface
3. Use Gog CLI directly with simple web wrapper

## Resources
- Roundcube: https://roundcube.net
- Gmail IMAP: https://support.google.com/mail/answer/7126229
- Gog CLI: https://github.com/openclaw/gog
- Mission Control Integration Guide