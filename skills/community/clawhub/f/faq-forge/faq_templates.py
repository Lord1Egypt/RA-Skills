#!/usr/bin/env python3
"""
FAQ Forge - Templates
Author: Shadow Rose
License: MIT
quality-verified

Pre-built FAQ templates for common business types.
Get started quickly with industry-standard questions.
"""

from typing import List, Dict
from faq_forge import FAQDatabase, FAQEntry


class FAQTemplates:
    """Pre-built FAQ templates for common business types."""
    
    TEMPLATES = {
        "digital-products": {
            "name": "Digital Products / Downloads",
            "description": "For selling ebooks, courses, software, templates, etc.",
            "categories": ["Getting Started", "Purchasing", "Downloads", "Technical Support", "Licensing"],
            "faqs": [
                {
                    "question": "How do I access my purchase after buying?",
                    "answer": "After completing your purchase, you'll receive an email with download links and access instructions. Check your spam folder if you don't see it within 5 minutes. You can also log into your account on our website to access your downloads anytime.",
                    "category": "Getting Started",
                    "tags": ["access", "download", "purchase"],
                    "priority": "high"
                },
                {
                    "question": "What payment methods do you accept?",
                    "answer": "We accept all major credit cards (Visa, Mastercard, American Express, Discover), PayPal, and Apple Pay. All transactions are securely processed through our payment provider.",
                    "category": "Purchasing",
                    "tags": ["payment", "security"],
                    "priority": "normal"
                },
                {
                    "question": "What is your refund policy?",
                    "answer": "We offer a 30-day money-back guarantee. If you're not satisfied with your purchase, contact us within 30 days for a full refund—no questions asked. Digital products cannot be returned after download, but we stand behind our quality.",
                    "category": "Purchasing",
                    "tags": ["refund", "guarantee"],
                    "priority": "high"
                },
                {
                    "question": "Can I download my purchase on multiple devices?",
                    "answer": "Yes! Your purchase is tied to your account, not your device. You can download and use your products on as many devices as you own for personal use. Commercial redistribution is not permitted.",
                    "category": "Downloads",
                    "tags": ["devices", "licensing"],
                    "priority": "normal"
                },
                {
                    "question": "I lost my download link. How do I get it again?",
                    "answer": "Log into your account and visit the Downloads section to access all your purchases. If you don't have an account or forgot your password, use the password reset option. Still having trouble? Contact support with your purchase email.",
                    "category": "Downloads",
                    "tags": ["download", "account", "support"],
                    "priority": "normal"
                },
                {
                    "question": "Do you offer updates for your products?",
                    "answer": "Yes! All updates and improvements are free for existing customers. When we release an update, you'll receive an email notification, and the latest version will be available in your account dashboard.",
                    "category": "Technical Support",
                    "tags": ["updates", "versions"],
                    "priority": "normal"
                },
                {
                    "question": "Can I use this product commercially?",
                    "answer": "Most of our products include commercial use rights, but licenses vary by product. Check the specific product page or license documentation included with your download. If you need extended licensing, contact us for options.",
                    "category": "Licensing",
                    "tags": ["commercial", "licensing", "rights"],
                    "priority": "high"
                }
            ]
        },
        
        "saas": {
            "name": "SaaS / Software as a Service",
            "description": "For subscription-based software and web applications.",
            "categories": ["Getting Started", "Account & Billing", "Features", "Technical Support", "Plans & Pricing"],
            "faqs": [
                {
                    "question": "How do I get started?",
                    "answer": "Sign up for a free trial on our homepage—no credit card required. After creating your account, you'll be guided through a quick onboarding process. Our getting started guide will walk you through the essential features.",
                    "category": "Getting Started",
                    "tags": ["signup", "trial", "onboarding"],
                    "priority": "critical"
                },
                {
                    "question": "Is there a free trial?",
                    "answer": "Yes! We offer a 14-day free trial with full access to all features. No credit card required to start. You can upgrade to a paid plan anytime, and your data will be preserved.",
                    "category": "Plans & Pricing",
                    "tags": ["trial", "pricing", "free"],
                    "priority": "high"
                },
                {
                    "question": "Can I cancel my subscription anytime?",
                    "answer": "Absolutely. You can cancel your subscription at any time from your account settings. Your access will continue until the end of your current billing period, and you won't be charged again. No cancellation fees.",
                    "category": "Account & Billing",
                    "tags": ["cancel", "subscription", "billing"],
                    "priority": "high"
                },
                {
                    "question": "How do I upgrade or downgrade my plan?",
                    "answer": "Go to Settings > Billing and select a new plan. Upgrades take effect immediately. Downgrades take effect at the end of your current billing cycle. You'll only pay the difference when upgrading mid-cycle.",
                    "category": "Plans & Pricing",
                    "tags": ["upgrade", "downgrade", "plans"],
                    "priority": "normal"
                },
                {
                    "question": "What happens to my data if I cancel?",
                    "answer": "Your data is safe! After cancellation, you have 60 days to export your data or reactivate your account. After 60 days, data is permanently deleted for security reasons. You can export your data anytime from your account.",
                    "category": "Account & Billing",
                    "tags": ["data", "cancel", "export"],
                    "priority": "high"
                },
                {
                    "question": "Do you offer team/multi-user accounts?",
                    "answer": "Yes! Our Team and Business plans support multiple users with role-based permissions. You can add or remove team members anytime, and billing is automatically adjusted. Contact us for custom enterprise pricing.",
                    "category": "Features",
                    "tags": ["team", "users", "collaboration"],
                    "priority": "normal"
                },
                {
                    "question": "Is my data secure?",
                    "answer": "Security is our top priority. All data is encrypted in transit (SSL/TLS) and at rest. We use industry-standard security practices, regular backups, and comply with GDPR and SOC 2 standards. Read our security page for full details.",
                    "category": "Technical Support",
                    "tags": ["security", "encryption", "privacy"],
                    "priority": "high"
                }
            ]
        },
        
        "freelance": {
            "name": "Freelance Services",
            "description": "For freelancers and service providers.",
            "categories": ["Getting Started", "Services & Pricing", "Process", "Payments", "Policies"],
            "faqs": [
                {
                    "question": "How do I get started working with you?",
                    "answer": "Reach out through the contact form with details about your project. I'll respond within 24 hours to discuss your needs, timeline, and budget. If we're a good fit, I'll send a proposal and contract to get started.",
                    "category": "Getting Started",
                    "tags": ["inquiry", "contact", "process"],
                    "priority": "critical"
                },
                {
                    "question": "What services do you offer?",
                    "answer": "I specialize in [your services]. Each project is unique, so I tailor my approach to your specific needs. Check out my portfolio for examples of past work and the results I've delivered for clients.",
                    "category": "Services & Pricing",
                    "tags": ["services", "offerings"],
                    "priority": "high"
                },
                {
                    "question": "How much do you charge?",
                    "answer": "Rates vary based on project scope, complexity, and timeline. I offer both hourly and project-based pricing. Contact me with your project details for a custom quote. My typical range is [your range], but I'm happy to work with various budgets.",
                    "category": "Services & Pricing",
                    "tags": ["pricing", "rates", "budget"],
                    "priority": "high"
                },
                {
                    "question": "What is your typical timeline?",
                    "answer": "Project timelines vary based on scope. Smaller projects typically take 1-2 weeks, while larger projects may take 4-8 weeks. I'll provide a detailed timeline in my proposal. Rush projects may be available for an additional fee.",
                    "category": "Process",
                    "tags": ["timeline", "delivery", "schedule"],
                    "priority": "normal"
                },
                {
                    "question": "Do you require a deposit?",
                    "answer": "Yes, I require a 50% deposit to begin work, with the remainder due upon completion. For larger projects, I offer milestone-based payment schedules. All payment terms are outlined in the contract before work begins.",
                    "category": "Payments",
                    "tags": ["deposit", "payment", "terms"],
                    "priority": "normal"
                },
                {
                    "question": "What payment methods do you accept?",
                    "answer": "I accept bank transfers, PayPal, and major credit cards. Payment details and invoicing will be handled through [your platform]. International payments are welcome.",
                    "category": "Payments",
                    "tags": ["payment", "methods"],
                    "priority": "normal"
                },
                {
                    "question": "What if I'm not happy with the work?",
                    "answer": "Client satisfaction is my top priority. I include revision rounds in all projects (typically 2-3 rounds depending on scope). If you're still not satisfied after revisions, we can discuss options. My goal is always to deliver work you're excited about.",
                    "category": "Policies",
                    "tags": ["revisions", "satisfaction", "guarantee"],
                    "priority": "high"
                },
                {
                    "question": "Do you sign NDAs or work under confidentiality?",
                    "answer": "Absolutely. I'm happy to sign NDAs and confidentiality agreements. I respect client privacy and never share project details without permission. All work is covered by a standard contract protecting both parties.",
                    "category": "Policies",
                    "tags": ["nda", "confidentiality", "contract"],
                    "priority": "normal"
                }
            ]
        },
        
        "ecommerce": {
            "name": "E-commerce / Physical Products",
            "description": "For online stores selling physical goods.",
            "categories": ["Ordering", "Shipping", "Returns & Refunds", "Products", "Support"],
            "faqs": [
                {
                    "question": "How long does shipping take?",
                    "answer": "Standard shipping takes 5-7 business days within the US. Express shipping (2-3 days) is available at checkout. International shipping typically takes 10-15 business days. You'll receive tracking information once your order ships.",
                    "category": "Shipping",
                    "tags": ["shipping", "delivery", "tracking"],
                    "priority": "critical"
                },
                {
                    "question": "What is your return policy?",
                    "answer": "We accept returns within 30 days of delivery for a full refund. Items must be unused and in original packaging. Return shipping is free for defective items; customer pays return shipping for other returns. Contact us to initiate a return.",
                    "category": "Returns & Refunds",
                    "tags": ["returns", "refund", "policy"],
                    "priority": "high"
                },
                {
                    "question": "Do you ship internationally?",
                    "answer": "Yes! We ship to most countries worldwide. Shipping costs and delivery times vary by location. International customers are responsible for any customs fees or import taxes. Check available countries at checkout.",
                    "category": "Shipping",
                    "tags": ["international", "shipping", "customs"],
                    "priority": "normal"
                },
                {
                    "question": "How can I track my order?",
                    "answer": "You'll receive a tracking number via email once your order ships. Click the tracking link to see real-time updates. You can also track your order by logging into your account and viewing order history.",
                    "category": "Ordering",
                    "tags": ["tracking", "order", "status"],
                    "priority": "high"
                },
                {
                    "question": "What if my item arrives damaged?",
                    "answer": "We're sorry if your item arrived damaged! Contact us within 48 hours with photos of the damage. We'll send a replacement immediately at no charge or issue a full refund—your choice. Keep the damaged item until we confirm receipt of your claim.",
                    "category": "Returns & Refunds",
                    "tags": ["damage", "replacement", "refund"],
                    "priority": "high"
                },
                {
                    "question": "Are your products authentic?",
                    "answer": "100% authentic guaranteed. We source directly from authorized distributors and manufacturers. Every product comes with authenticity verification. If you ever receive a counterfeit item, we'll refund you double your purchase price.",
                    "category": "Products",
                    "tags": ["authentic", "genuine", "quality"],
                    "priority": "high"
                }
            ]
        }
    }
    
    def __init__(self, db: FAQDatabase):
        self.db = db
    
    def list_templates(self):
        """Display available templates."""
        print("\nAvailable FAQ Templates:\n")
        for key, template in self.TEMPLATES.items():
            print(f"  {key}")
            print(f"    {template['name']}")
            print(f"    {template['description']}")
            print(f"    {len(template['faqs'])} questions\n")
    
    def apply_template(self, template_key: str, product: str = "default",
                       customize: bool = True) -> int:
        """
        Apply a template to the FAQ database.
        Returns number of entries added.
        """
        if template_key not in self.TEMPLATES:
            print(f"Error: Template '{template_key}' not found")
            return 0
        
        template = self.TEMPLATES[template_key]
        
        if customize:
            print(f"\nApplying template: {template['name']}")
            print(f"{template['description']}\n")
            print("These questions are templates. You'll want to customize them with your specific:")
            print("  - Business details")
            print("  - Policies and timelines")
            print("  - Pricing and terms")
            print("  - Contact information\n")
        
        added = 0
        for faq_data in template['faqs']:
            entry = FAQEntry(
                question=faq_data['question'],
                answer=faq_data['answer'],
                category=faq_data['category'],
                tags=faq_data['tags'],
                priority=faq_data['priority'],
                product=product
            )
            
            # Mark template entries for review
            entry.feedback = {
                "needs_improvement": customize,
                "outdated": False,
                "notes": "Template entry - customize with your specific business details"
            }
            
            self.db.add(entry)
            added += 1
        
        print(f"✓ Added {added} FAQ entries from '{template['name']}' template")
        
        if customize:
            print("\nNext steps:")
            print("  1. Review each question: faq_forge.py search --category [category]")
            print("  2. Customize answers: faq_forge.py update <id> --answer 'Your specific answer'")
            print("  3. Add your own questions: faq_forge.py add <question> <answer>")
            print("  4. Publish: faq_publish.py html output.html")
        
        return added


def main():
    """Command-line interface for FAQ templates."""
    import sys
    
    if len(sys.argv) < 2:
        print("FAQ Forge Templates")
        print("\nUsage:")
        print("  faq_templates.py list")
        print("  faq_templates.py apply <template-key> [--product PROD] [--no-customize-prompt]")
        print("\nAvailable templates:")
        print("  digital-products    - Digital downloads, courses, ebooks")
        print("  saas               - Software as a Service applications")
        print("  freelance          - Freelance services and consulting")
        print("  ecommerce          - Physical products and online stores")
        return
    
    db = FAQDatabase()
    templates = FAQTemplates(db)
    
    command = sys.argv[1]
    
    if command == "list":
        templates.list_templates()
    
    elif command == "apply":
        if len(sys.argv) < 3:
            print("Error: apply requires <template-key>")
            return
        
        template_key = sys.argv[2]
        product = "default"
        customize = True
        
        for i in range(3, len(sys.argv)):
            if sys.argv[i] == "--product" and i + 1 < len(sys.argv):
                product = sys.argv[i + 1]
            elif sys.argv[i] == "--no-customize-prompt":
                customize = False
        
        templates.apply_template(template_key, product, customize)
    
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
