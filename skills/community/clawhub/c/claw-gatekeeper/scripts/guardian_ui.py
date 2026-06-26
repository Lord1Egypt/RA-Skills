#!/usr/bin/env python3
"""
Claw-Gatekeeper User Interface
Handles user interaction for operation confirmation with session-level support

Features:
- Interactive confirmation prompts with rich formatting
- Session-level auto-approval for MEDIUM/HIGH after user confirmation
- Per-confirmation option for CRITICAL risks
- Comprehensive audit logging
"""

import os
import json
import sys
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass, asdict

# Import session manager
from session_manager import SessionManager, SessionPermission


class UserDecision(Enum):
    """User decision types"""
    ALLOW_ONCE = "allow_once"
    ALLOW_SESSION = "allow_session"  # For MEDIUM/HIGH - allow for entire session
    ALLOW_ALWAYS = "allow_always"
    DENY_ONCE = "deny_once"
    DENY_ALWAYS = "deny_always"
    VIEW_DETAILS = "view_details"


@dataclass
class GuardianRequest:
    """Request for user confirmation"""
    operation_type: str
    operation_detail: str
    risk_level: str
    risk_score: int
    risk_reasons: List[str]
    recommendation: str
    timestamp: str


@dataclass
class GuardianResponse:
    """User response to confirmation request"""
    decision: str
    request: GuardianRequest
    response_time: str
    user_comment: Optional[str] = None
    add_to_whitelist: bool = False
    add_to_blacklist: bool = False
    session_approved: bool = False


class GuardianUI:
    """Interactive confirmation UI with rich formatting and session support"""
    
    # Risk level visual indicators
    RISK_DISPLAY = {
        "CRITICAL": ("🔴", "\033[91m"),  # Red
        "HIGH": ("🟠", "\033[93m"),      # Yellow/Orange
        "MEDIUM": ("🟡", "\033[94m"),    # Blue/Yellow
        "LOW": ("🟢", "\033[92m"),       # Green
    }
    
    RESET_COLOR = "\033[0m"
    
    # Operation type display names
    OPERATION_NAMES = {
        "file": "📁 File Operation",
        "shell": "💻 Shell Command",
        "network": "🌐 Network Request",
        "skill": "📦 Skill Installation",
        "system": "⚙️  System Configuration"
    }
    
    # Risk levels that support session approval
    SESSION_APPROVAL_RISKS = ["MEDIUM", "HIGH"]
    ALWAYS_CONFIRM_RISKS = ["CRITICAL"]
    AUTO_ALLOW_RISKS = ["LOW"]
    
    def __init__(self, log_dir: Optional[str] = None, use_colors: bool = True):
        self.log_dir = log_dir or os.path.expanduser("~/.claw-gatekeeper/logs")
        os.makedirs(self.log_dir, exist_ok=True)
        self.use_colors = use_colors and sys.stdout.isatty()
        
        # Initialize session manager
        self.session_manager = SessionManager()
    
    def _colorize(self, text: str, color_code: str) -> str:
        """Apply color if colors are enabled"""
        if self.use_colors:
            return f"{color_code}{text}{self.RESET_COLOR}"
        return text
    
    def check_permission(self, request: GuardianRequest) -> Tuple[bool, str, bool]:
        """
        Check if operation is permitted without user interaction
        
        Returns:
            (is_allowed, reason, needs_interaction)
        """
        risk_level = request.risk_level
        
        # LOW risk: auto-allow
        if risk_level in self.AUTO_ALLOW_RISKS:
            return True, "LOW risk - auto-allowed", False
        
        # CRITICAL risk: always requires confirmation
        if risk_level in self.ALWAYS_CONFIRM_RISKS:
            return False, "CRITICAL risk - always requires confirmation", True
        
        # MEDIUM/HIGH: check session permission
        if risk_level in self.SESSION_APPROVAL_RISKS:
            allowed, reason = self.session_manager.check_session_permission(
                request.operation_type,
                risk_level,
                request.operation_detail
            )
            
            if allowed:
                # Session approved - log and allow
                self._log_audit(request, "allow_session", reason)
                return True, reason, False
            else:
                # Needs user confirmation
                return False, reason, True
        
        # Unknown risk level - require confirmation
        return False, "Unknown risk level - requires confirmation", True
    
    def format_interruption(self, request: GuardianRequest, compact: bool = False) -> str:
        """Format the interruption message with rich visual elements"""
        op_name = self.OPERATION_NAMES.get(request.operation_type, f"📋 {request.operation_type.title()}")
        emoji, color = self.RISK_DISPLAY.get(request.risk_level, ("⚪", ""))
        
        if compact:
            return f"{emoji} [{request.risk_level}] {op_name}: {request.operation_detail[:50]}..."
        
        # Full format
        lines = [
            "",
            "=" * 70,
            "🛡️  CLAW-GUARDIAN SECURITY INTERCEPTION",
            "=" * 70,
            "",
            f"📋 Operation: {op_name}",
            f"📝 Detail: {request.operation_detail}",
            "",
        ]
        
        # Risk level with color
        risk_display = f"{emoji}  Risk Level: {request.risk_level}"
        if color:
            risk_display = self._colorize(risk_display, color)
        lines.append(risk_display)
        
        lines.append(f"📊 Risk Score: {request.risk_score}/100")
        lines.append("")
        
        # Risk reasons
        if request.risk_reasons:
            lines.append("⚠️  Risk Analysis:")
            for i, reason in enumerate(request.risk_reasons, 1):
                lines.append(f"   {i}. {reason}")
            lines.append("")
        
        # Recommendation
        lines.append(f"💡 Recommendation: {request.recommendation}")
        lines.append("")
        
        # Session info for MEDIUM/HIGH
        if request.risk_level in self.SESSION_APPROVAL_RISKS:
            session_info = self.session_manager.get_session_info()
            if session_info['active_approvals'] > 0:
                lines.append(f"📌 Session has {session_info['active_approvals']} active approval(s)")
                lines.append("")
        
        # Action options
        lines.extend([
            "-" * 70,
            "SELECT AN OPTION:",
            "",
        ])
        
        # Different options based on risk level
        if request.risk_level == "CRITICAL":
            lines.extend([
                "   [y] ✅ Allow this time (CRITICAL - must confirm each time)",
                "   [Y] ✅✅ Always allow (add to whitelist)",
                "   [n] ❌ Deny this time",
                "   [N] ❌❌ Always deny (add to blacklist)",
            ])
        else:  # MEDIUM or HIGH
            lines.extend([
                "   [y] ✅ Allow this time only",
                "   [s] ✅📅 Allow for this session (auto-approve similar operations)",
                "   [Y] ✅✅ Always allow (add to whitelist)",
                "   [n] ❌ Deny this time",
                "   [N] ❌❌ Always deny (add to blacklist)",
            ])
        
        lines.extend([
            "   [?] ℹ️  View details",
            "   [h] ❓ Help",
            "",
            "-" * 70,
            "Your choice: "
        ])
        
        return "\n".join(lines)
    
    def interactive_confirm(self, request: GuardianRequest, 
                           timeout: Optional[int] = None) -> GuardianResponse:
        """
        Display interactive confirmation prompt and get user decision
        
        For MEDIUM/HIGH: Offers session-level approval option
        For CRITICAL: Must confirm each time
        """
        prompt = self.format_interruption(request)
        
        start_time = datetime.now()
        
        while True:
            try:
                choice = input(prompt).strip().lower()
                
                # Handle timeout
                if timeout:
                    elapsed = (datetime.now() - start_time).total_seconds()
                    if elapsed > timeout:
                        print("\n⏱️  Confirmation timeout - operation denied for safety")
                        decision = UserDecision.DENY_ONCE
                        comment = "Auto-denied due to timeout"
                        session_approved = False
                        break
                
                if choice == 'y':
                    decision = UserDecision.ALLOW_ONCE
                    comment = "User approved single execution"
                    session_approved = False
                    break
                    
                elif choice == 's' and request.risk_level in self.SESSION_APPROVAL_RISKS:
                    # Session-level approval only for MEDIUM/HIGH
                    decision = UserDecision.ALLOW_SESSION
                    comment = "User approved for this session"
                    session_approved = True
                    
                    # Grant session approval
                    self.session_manager.grant_session_approval(
                        request.operation_type,
                        request.risk_level,
                        request.operation_detail,
                        "session"
                    )
                    break
                    
                elif choice == 'Y':
                    decision = UserDecision.ALLOW_ALWAYS
                    comment = "User approved and added to whitelist"
                    session_approved = False
                    break
                    
                elif choice == 'n':
                    decision = UserDecision.DENY_ONCE
                    comment = "User denied execution"
                    session_approved = False
                    break
                    
                elif choice == 'N':
                    decision = UserDecision.DENY_ALWAYS
                    comment = "User denied and added to blacklist"
                    session_approved = False
                    break
                    
                elif choice == '?':
                    self._show_details(request)
                    prompt = self.format_interruption(request)
                    continue
                    
                elif choice == 'h' or choice == 'help':
                    self._show_help(request.risk_level)
                    prompt = self.format_interruption(request)
                    continue
                    
                elif choice == '':
                    print("\n⚠️  No input received - operation denied for safety")
                    decision = UserDecision.DENY_ONCE
                    comment = "Auto-denied (no input)"
                    session_approved = False
                    break
                    
                else:
                    if choice == 's' and request.risk_level == "CRITICAL":
                        print(f"\n❌ Session approval not available for CRITICAL risks")
                        print("CRITICAL operations must be confirmed each time.")
                    else:
                        print(f"\n❌ Invalid choice: '{choice}'")
                        valid_options = "y, Y, n, N, ?, h"
                        if request.risk_level in self.SESSION_APPROVAL_RISKS:
                            valid_options += ", s"
                        print(f"Valid options: {valid_options}")
                    prompt = "Your choice: "
                    continue
                    
            except KeyboardInterrupt:
                print("\n\n🚫 Operation cancelled by user (Ctrl+C)")
                decision = UserDecision.DENY_ONCE
                comment = "User cancelled (KeyboardInterrupt)"
                session_approved = False
                break
                
            except EOFError:
                print("\n⚠️  Non-interactive environment - defaulting to DENY for safety")
                decision = UserDecision.DENY_ONCE
                comment = "Auto-denied in non-interactive mode"
                session_approved = False
                break
        
        response = GuardianResponse(
            decision=decision.value,
            request=request,
            response_time=datetime.now().isoformat(),
            user_comment=comment,
            add_to_whitelist=(decision == UserDecision.ALLOW_ALWAYS),
            add_to_blacklist=(decision == UserDecision.DENY_ALWAYS),
            session_approved=session_approved
        )
        
        self._log_decision(response)
        self._log_audit(request, response.decision, comment)
        
        # Print confirmation
        if decision in [UserDecision.ALLOW_ONCE, UserDecision.ALLOW_SESSION, 
                       UserDecision.ALLOW_ALWAYS]:
            print(f"\n✅ Operation {self._colorize('APPROVED', '\033[92m')}")
            if session_approved:
                print(f"📌 Similar {request.risk_level} risk operations will be auto-approved for this session")
        else:
            print(f"\n❌ Operation {self._colorize('DENIED', '\033[91m')}")
        
        return response
    
    def auto_decide(self, request: GuardianRequest, 
                   default_allow_low: bool = True,
                   default_allow_medium: bool = False,
                   default_allow_high: bool = False) -> GuardianResponse:
        """
        Automatic decision for non-interactive environments
        """
        risk_level = request.risk_level
        
        if risk_level == "CRITICAL":
            decision = UserDecision.DENY_ONCE
            comment = "CRITICAL risk auto-denied in non-interactive mode"
            
        elif risk_level == "HIGH":
            if default_allow_high:
                decision = UserDecision.ALLOW_ONCE
                comment = "HIGH risk auto-allowed (configured)"
            else:
                decision = UserDecision.DENY_ONCE
                comment = "HIGH risk auto-denied (default)"
                
        elif risk_level == "MEDIUM":
            if default_allow_medium:
                decision = UserDecision.ALLOW_ONCE
                comment = "MEDIUM risk auto-allowed (configured)"
            else:
                decision = UserDecision.DENY_ONCE
                comment = "MEDIUM risk auto-denied (default)"
                
        else:  # LOW
            if default_allow_low:
                decision = UserDecision.ALLOW_ONCE
                comment = "LOW risk auto-allowed"
            else:
                decision = UserDecision.DENY_ONCE
                comment = "LOW risk auto-denied (configured)"
        
        response = GuardianResponse(
            decision=decision.value,
            request=request,
            response_time=datetime.now().isoformat(),
            user_comment=comment
        )
        
        self._log_decision(response)
        self._log_audit(request, response.decision, comment)
        
        status = "APPROVED" if "allow" in decision.value else "DENIED"
        print(f"[AUTO] {request.operation_type}: {status} ({risk_level})")
        
        return response
    
    def _show_details(self, request: GuardianRequest):
        """Show detailed information about the operation"""
        print("\n" + "=" * 70)
        print("DETAILED INFORMATION")
        print("=" * 70)
        print(f"Timestamp: {request.timestamp}")
        print(f"Operation Type: {request.operation_type}")
        print(f"Risk Level: {request.risk_level}")
        print(f"Risk Score: {request.risk_score}/100")
        
        if request.risk_score >= 80:
            print("\n⚠️  This is a CRITICAL risk operation!")
            print("Such operations can cause serious damage or data loss.")
            print("You must confirm EACH CRITICAL operation individually.")
        elif request.risk_score >= 60:
            print("\n⚠️  This is a HIGH risk operation!")
            print("Proceed with caution and verify the intent.")
            print("You can approve for this session to avoid repeated prompts.")
        elif request.risk_score >= 30:
            print("\n⚠️  This is a MEDIUM risk operation.")
            print("Some risk exists, but it's generally manageable.")
            print("Session approval is available.")
        
        print("\nFull Risk Analysis:")
        for i, reason in enumerate(request.risk_reasons, 1):
            print(f"  {i}. {reason}")
        
        print("\nSafety Recommendation:")
        print(f"  {request.recommendation}")
        
        # Show current session info
        session_info = self.session_manager.get_session_info()
        if session_info['active_approvals'] > 0:
            print(f"\n📌 Current Session Approvals: {session_info['active_approvals']}")
            for approval in session_info['approvals'][:5]:
                print(f"   - [{approval['risk']}] {approval['type']}: {approval['pattern'][:40]}")
        
        print("\n" + "=" * 70)
        print("\nPress Enter to return to confirmation prompt...")
        try:
            input()
        except (KeyboardInterrupt, EOFError):
            pass
        print()
    
    def _show_help(self, risk_level: str):
        """Show help information"""
        print("\n" + "=" * 70)
        print("CLAW-GUARDIAN HELP")
        print("=" * 70)
        print("""
Claw-Guardian protects your system by intercepting potentially
dangerous operations from OpenClaw.

OPTIONS:
  [y] - Allow this operation once
        The operation proceeds, but you'll be asked again next time.
  
  [s] - Allow for this session (MEDIUM/HIGH only)
        Similar operations will be auto-approved for this session.
        The session expires after 30 minutes of inactivity.
        NOT available for CRITICAL risks.
  
  [Y] - Always allow (add to whitelist)
        This operation type will be allowed automatically in the future.
        Use for trusted operations you do frequently.
  
  [n] - Deny this operation
        The operation is blocked, but can be retried later.
  
  [N] - Always deny (add to blacklist)
        This operation type will be blocked automatically.
        Use for operations you never want to allow.
  
  [?] - View details
        See more information about the risks and operation details.

RISK LEVELS:
  🔴 CRITICAL (80-100) - System-level danger
        ALWAYS requires confirmation each time
        Session approval is NOT available
  
  🟠 HIGH (60-79) - Sensitive operations
        Requires confirmation or session approval
        Session approval available
  
  🟡 MEDIUM (30-59) - General risk
        Suggests confirmation or session approval
        Session approval available
  
  🟢 LOW (0-29) - Safe operations
        Auto-allowed without confirmation

For more information, see the documentation.
        """)
        print("=" * 70)
        print("\nPress Enter to return...")
        try:
            input()
        except (KeyboardInterrupt, EOFError):
            pass
        print()
    
    def _log_decision(self, response: GuardianResponse):
        """Log the decision to file"""
        log_file = os.path.join(self.log_dir, 
                               f"decisions_{datetime.now().strftime('%Y%m')}.jsonl")
        
        log_entry = {
            "timestamp": response.response_time,
            "decision": response.decision,
            "operation": asdict(response.request),
            "comment": response.user_comment,
            "whitelist_added": response.add_to_whitelist,
            "blacklist_added": response.add_to_blacklist,
            "session_approved": response.session_approved
        }
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"Warning: Could not log decision: {e}", file=os.sys.stderr)
    
    def _log_audit(self, request: GuardianRequest, decision: str, comment: str):
        """Log to Operate_Audit.log (MEDIUM and above only)"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "risk_level": request.risk_level,
            "risk_score": request.risk_score,
            "operation_type": request.operation_type,
            "operation_detail": request.operation_detail,
            "decision": decision,
            "comment": comment
        }
        
        self.session_manager.write_audit_log(entry)


def main():
    """Command-line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Claw-Guardian UI")
    parser.add_argument("command", choices=["interactive", "auto", "check", "session"])
    parser.add_argument("request", nargs="?", help="JSON request or file path")
    parser.add_argument("--default-allow-low", type=lambda x: x.lower() == 'true',
                       default=True)
    parser.add_argument("--default-allow-medium", type=lambda x: x.lower() == 'true',
                       default=False)
    parser.add_argument("--default-allow-high", type=lambda x: x.lower() == 'true',
                       default=False)
    
    args = parser.parse_args()
    
    ui = GuardianUI()
    
    if args.command == "interactive":
        if not args.request:
            print("Error: request JSON required")
            sys.exit(1)
        
        if os.path.isfile(args.request):
            with open(args.request, 'r') as f:
                data = json.load(f)
        else:
            data = json.loads(args.request)
        
        request = GuardianRequest(**data)
        
        # First check if permission already granted
        allowed, reason, needs_interaction = ui.check_permission(request)
        
        if allowed:
            print(f"✅ {reason}")
            result = {
                "approved": True,
                "decision": "allow_session",
                "reason": reason
            }
            print(json.dumps(result, indent=2))
            sys.exit(0)
        elif not needs_interaction:
            print(f"❌ {reason}")
            result = {
                "approved": False,
                "decision": "deny",
                "reason": reason
            }
            print(json.dumps(result, indent=2))
            sys.exit(1)
        
        # Need user interaction
        response = ui.interactive_confirm(request)
        
        result = {
            "approved": "allow" in response.decision,
            "decision": response.decision,
            "session_approved": response.session_approved,
            "comment": response.user_comment
        }
        print(json.dumps(result, indent=2))
        sys.exit(0 if result["approved"] else 1)
    
    elif args.command == "auto":
        if not args.request:
            print("Error: request JSON required")
            sys.exit(1)
        
        if os.path.isfile(args.request):
            with open(args.request, 'r') as f:
                data = json.load(f)
        else:
            data = json.loads(args.request)
        
        request = GuardianRequest(**data)
        response = ui.auto_decide(request, args.default_allow_low, 
                                  args.default_allow_medium,
                                  args.default_allow_high)
        
        result = {
            "approved": "allow" in response.decision,
            "decision": response.decision,
            "comment": response.user_comment
        }
        print(json.dumps(result, indent=2))
        sys.exit(0 if result["approved"] else 1)
    
    elif args.command == "check":
        # Check permission without interaction
        if not args.request:
            print("Error: request JSON required")
            sys.exit(1)
        
        if os.path.isfile(args.request):
            with open(args.request, 'r') as f:
                data = json.load(f)
        else:
            data = json.loads(args.request)
        
        request = GuardianRequest(**data)
        allowed, reason, needs_interaction = ui.check_permission(request)
        
        result = {
            "allowed": allowed,
            "needs_interaction": needs_interaction,
            "reason": reason
        }
        print(json.dumps(result, indent=2))
        sys.exit(0 if allowed else 1)
    
    elif args.command == "session":
        # Show session info
        info = ui.session_manager.get_session_info()
        print(json.dumps(info, indent=2))
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
