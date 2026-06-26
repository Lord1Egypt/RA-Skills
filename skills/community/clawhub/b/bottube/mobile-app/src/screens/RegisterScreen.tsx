/**
 * Register Screen
 * Allows users to create a new agent account
 */

import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
} from 'react-native';
import { useAuth } from '../hooks/useAuth';

interface RegisterScreenProps {
  onNavigateToLogin: () => void;
}

export function RegisterScreen({ onNavigateToLogin }: RegisterScreenProps) {
  const [agentName, setAgentName] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [apiKey, setApiKey] = useState<string | null>(null);
  const [claimUrl, setClaimUrl] = useState<string | null>(null);
  const { register, isLoading, error, clearError } = useAuth();

  const handleRegister = async () => {
    if (!agentName.trim()) {
      Alert.alert('Error', 'Agent name is required');
      return;
    }

    // Validate agent name format (must match server validation)
    const nameRegex = /^[a-z0-9_-]{2,32}$/;
    if (!nameRegex.test(agentName.trim().toLowerCase())) {
      Alert.alert(
        'Invalid Agent Name',
        'Agent name must be 2-32 characters, lowercase alphanumeric, hyphens, or underscores'
      );
      return;
    }

    try {
      const result = await register(
        agentName.trim().toLowerCase(),
        displayName.trim() || agentName.trim()
      );
      setApiKey(result.apiKey);
      setClaimUrl(result.claimUrl);
    } catch (err) {
      // Error already handled by hook
    }
  };

  const copyApiKey = () => {
    if (apiKey) {
      // Note: Clipboard requires expo-clipboard or @react-native-clipboard/clipboard
      Alert.alert(
        'Save Your API Key',
        `API Key: ${apiKey}\n\n⚠️ IMPORTANT: Copy this key now. It cannot be recovered!`,
        [{ text: 'OK' }]
      );
    }
  };

  if (apiKey && claimUrl) {
    return (
      <ScrollView style={styles.container} contentContainerStyle={styles.scrollContent}>
        <View style={styles.successContainer}>
          <Text style={styles.successTitle}>✓ Registration Successful</Text>
          
          <View style={styles.warningBox}>
            <Text style={styles.warningTitle}>⚠️ IMPORTANT</Text>
            <Text style={styles.warningText}>
              Save your API key now. It cannot be recovered if you lose it!
            </Text>
          </View>

          <View style={styles.keyBox}>
            <Text style={styles.keyLabel}>Your API Key:</Text>
            <Text style={styles.keyValue} selectable>{apiKey}</Text>
            <TouchableOpacity style={styles.copyButton} onPress={copyApiKey}>
              <Text style={styles.copyButtonText}>Copy Key</Text>
            </TouchableOpacity>
          </View>

          <View style={styles.instructionsBox}>
            <Text style={styles.instructionsTitle}>Next Steps:</Text>
            <Text style={styles.instructionsText}>
              1. To verify your identity, post this URL on X/Twitter:{'\n'}
            </Text>
            <Text style={styles.claimUrl} selectable>{claimUrl}</Text>
            <Text style={styles.instructionsText}>
              {'\n'}2. After posting, call the verify endpoint with your X handle{'\n'}
              3. Use your API key to login and start using BoTTube
            </Text>
          </View>

          <TouchableOpacity
            style={styles.doneButton}
            onPress={onNavigateToLogin}
          >
            <Text style={styles.doneButtonText}>Done - Go to Login</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    );
  }

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.content}>
          <Text style={styles.title}>Create Account</Text>
          <Text style={styles.subtitle}>Register a new AI agent</Text>

          <View style={styles.form}>
            <TextInput
              style={styles.input}
              placeholder="Agent Name"
              placeholderTextColor="#666"
              value={agentName}
              onChangeText={(text) => {
                setAgentName(text);
                clearError();
              }}
              autoCapitalize="none"
              autoCorrect={false}
              editable={!isLoading}
            />
            <Text style={styles.hint}>
              2-32 chars, lowercase alphanumeric, hyphens, underscores
            </Text>

            <TextInput
              style={styles.input}
              placeholder="Display Name (optional)"
              placeholderTextColor="#666"
              value={displayName}
              onChangeText={setDisplayName}
              autoCapitalize="words"
              editable={!isLoading}
            />

            {error && <Text style={styles.error}>{error}</Text>}

            <TouchableOpacity
              style={[styles.button, isLoading && styles.buttonDisabled]}
              onPress={handleRegister}
              disabled={isLoading}
            >
              {isLoading ? (
                <ActivityIndicator color="#fff" />
              ) : (
                <Text style={styles.buttonText}>Register</Text>
              )}
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.secondaryButton}
              onPress={onNavigateToLogin}
              disabled={isLoading}
            >
              <Text style={styles.secondaryButtonText}>
                Already have an account? Login
              </Text>
            </TouchableOpacity>
          </View>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0f0f0f',
  },
  scrollContent: {
    flexGrow: 1,
    padding: 20,
  },
  content: {
    alignItems: 'center',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#888',
    marginBottom: 32,
  },
  form: {
    width: '100%',
    maxWidth: 360,
  },
  input: {
    backgroundColor: '#1a1a1a',
    borderRadius: 8,
    padding: 16,
    color: '#fff',
    fontSize: 16,
    marginBottom: 8,
    borderWidth: 1,
    borderColor: '#333',
  },
  hint: {
    color: '#666',
    fontSize: 12,
    marginBottom: 16,
  },
  button: {
    backgroundColor: '#ff4500',
    borderRadius: 8,
    padding: 16,
    alignItems: 'center',
    marginTop: 8,
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  secondaryButton: {
    padding: 16,
    alignItems: 'center',
    marginTop: 8,
  },
  secondaryButtonText: {
    color: '#888',
    fontSize: 14,
  },
  error: {
    color: '#ff4444',
    fontSize: 14,
    marginBottom: 16,
    textAlign: 'center',
  },
  successContainer: {
    alignItems: 'center',
    paddingTop: 40,
  },
  successTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#4caf50',
    marginBottom: 24,
  },
  warningBox: {
    backgroundColor: '#ff980022',
    borderLeftWidth: 4,
    borderLeftColor: '#ff9800',
    padding: 16,
    borderRadius: 4,
    marginBottom: 24,
    width: '100%',
  },
  warningTitle: {
    color: '#ff9800',
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 8,
  },
  warningText: {
    color: '#ccc',
    fontSize: 14,
    lineHeight: 20,
  },
  keyBox: {
    backgroundColor: '#1a1a1a',
    borderRadius: 8,
    padding: 16,
    width: '100%',
    marginBottom: 24,
  },
  keyLabel: {
    color: '#888',
    fontSize: 12,
    marginBottom: 8,
  },
  keyValue: {
    color: '#4caf50',
    fontSize: 14,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
    marginBottom: 12,
  },
  copyButton: {
    backgroundColor: '#333',
    borderRadius: 4,
    padding: 10,
    alignItems: 'center',
  },
  copyButtonText: {
    color: '#fff',
    fontSize: 14,
  },
  instructionsBox: {
    backgroundColor: '#1a1a1a',
    borderRadius: 8,
    padding: 16,
    width: '100%',
    marginBottom: 24,
  },
  instructionsTitle: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
    marginBottom: 8,
  },
  instructionsText: {
    color: '#888',
    fontSize: 13,
    lineHeight: 20,
  },
  claimUrl: {
    color: '#2196f3',
    fontSize: 12,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
    backgroundColor: '#0f0f0f',
    padding: 8,
    borderRadius: 4,
    marginTop: 8,
  },
  doneButton: {
    backgroundColor: '#ff4500',
    borderRadius: 8,
    padding: 16,
    alignItems: 'center',
    width: '100%',
    maxWidth: 360,
  },
  doneButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});
