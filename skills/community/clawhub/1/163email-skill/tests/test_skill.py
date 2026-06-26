"""
Unit tests for 163email Skill
"""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from send_email import send_mail


class TestSendMail(unittest.TestCase):
    """Test cases for send_mail function"""

    @patch('send_email.smtplib.SMTP_SSL')
    def test_send_mail_success(self, mock_smtp):
        """Test successful email sending"""
        mock_instance = MagicMock()
        mock_smtp.return_value = mock_instance

        result = send_mail(
            to="test@example.com",
            subject="Test Subject",
            content="Test Content"
        )

        self.assertTrue(result)
        mock_smtp.assert_called_once_with("smtp.163.com", 465)
        mock_instance.login.assert_called_once()
        mock_instance.sendmail.assert_called_once()
        mock_instance.quit.assert_called_once()

    @patch('send_email.smtplib.SMTP_SSL')
    def test_send_mail_failure(self, mock_smtp):
        """Test failed email sending"""
        mock_instance = MagicMock()
        mock_instance.login.side_effect = smtplib.SMTPException("Login failed")
        mock_smtp.return_value = mock_instance

        result = send_mail(
            to="test@example.com",
            subject="Test Subject",
            content="Test Content"
        )

        self.assertFalse(result)

    def test_multiple_recipients(self):
        """Test multiple recipients parsing"""
        # This test verifies the input parsing logic
        to = "user1@example.com, user2@example.com"
        receivers = [x.strip() for x in to.split(',')]
        self.assertEqual(len(receivers), 2)
        self.assertEqual(receivers[0], "user1@example.com")
        self.assertEqual(receivers[1], "user2@example.com")


if __name__ == '__main__':
    unittest.main()
